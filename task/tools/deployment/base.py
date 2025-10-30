import json
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

from aidial_client import AsyncDial
from aidial_sdk.chat_completion import Message, Role, CustomContent
from pydantic import StrictStr

from task.tools.base_tool import BaseTool
from task.tools.models import ToolCallParams


class DeploymentTool(BaseTool, ABC):

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @property
    @abstractmethod
    def deployment_name(self) -> str:
        pass

    @property
    def tool_parameters(self) -> dict[str, Any]:
        return {}

    @property
    @abstractmethod
    def _state_key_name(self) -> str:
        pass

    def _prepare_messages(self, tool_call_params: ToolCallParams) -> list[dict[str, Any]]:
        arguments = json.loads(tool_call_params.tool_call.function.arguments)
        prompt = arguments["prompt"]
        propagate_history = bool(arguments["propagate_history"])

        messages = []

        if propagate_history:
            for idx in range(len(tool_call_params.messages)):
                msg = tool_call_params.messages[idx]
                if msg.role == Role.ASSISTANT:
                    if msg.custom_content and msg.custom_content.state:
                        msg_state = msg.custom_content.state
                        if msg_state.get(self._state_key_name):
                            # 1. add user request (user message is always before assistant message)
                            messages.append(tool_call_params.messages[idx-1].dict(exclude_none=True))

                            # 2. Copy assistant message
                            copied_msg = deepcopy(msg)
                            copied_msg.custom_content.state = msg_state.get(self._state_key_name)
                            messages.append(copied_msg.dict(exclude_none=True))
        else:
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                    "custom_content": tool_call_params.messages[-1].custom_content.dict(exclude_none=True),
                }
            ]

        return messages

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        client: AsyncDial = AsyncDial(
            base_url=self.endpoint,
            api_key=tool_call_params.api_key,
        )

        arguments = json.loads(tool_call_params.tool_call.function.arguments)
        if arguments.get("prompt"):
            del arguments["prompt"]

        chunks = await client.chat.completions.create(
            messages=self._prepare_messages(tool_call_params),
            stream=True,
            deployment_name=self.deployment_name,
            extra_body={
                "custom_fields": {
                    "configuration": {**arguments}
                }
            },
            **self.tool_parameters,
        )

        content = ''
        custom_content: CustomContent = CustomContent(attachments=[])
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta:
                    if delta.content:
                        tool_call_params.stage.append_content(delta.content)
                        content += delta.content
                    if delta.custom_content and delta.custom_content.attachments:
                        attachments = delta.custom_content.attachments
                        custom_content.attachments.extend(attachments)

                        for attachment in attachments:
                            tool_call_params.stage.add_attachment(
                                type=attachment.type,
                                title=attachment.title,
                                data=attachment.data,
                                url=attachment.url,
                                reference_url=attachment.reference_url,
                                reference_type=attachment.reference_type,
                            )

        return Message(
            role=Role.TOOL,
            content=StrictStr(content),
            custom_content=custom_content,
            tool_call_id=StrictStr(tool_call_params.tool_call.id),
        )

