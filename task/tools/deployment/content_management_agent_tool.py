from typing import Any

from aidial_sdk.chat_completion import Message

from task.tools.deployment.base import DeploymentTool
from task.tools.models import ToolCallParams
from task.utils.constants import TOOL_CALL_HISTORY_KEY, CONTENT_MANAGEMENT_AGENT_HISTORY_KEY


class ContentManagementAgentTool(DeploymentTool):

    @property
    def _state_key_name(self) -> str:
        return CONTENT_MANAGEMENT_AGENT_HISTORY_KEY

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        msg = await super()._execute(tool_call_params)

        if msg.custom_content and msg.custom_content.state and msg.custom_content.state.get(TOOL_CALL_HISTORY_KEY):
            msg.custom_content.state = {
                CONTENT_MANAGEMENT_AGENT_HISTORY_KEY: msg.custom_content.state
            }

        return msg

    @property
    def deployment_name(self) -> str:
        return "content-management-agent"

    @property
    def name(self) -> str:
        return "content_management_agent_tool"

    @property
    def description(self) -> str:
        return "Agent to work with files. Extract and analyze files content, performs RAG Search through files content."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The query or instruction to send to the Content Management Agent."
                },
                "propagate_history": {
                    "type": "boolean",
                    "default": False,
                    "description": ("Whether to include previous conversation history between the current agent and Content Management Agent. "
                                    "When `true`, the Content Management Agent will have access to prior exchanges for context continuity. "
                                    "When `false`, each call starts fresh without historical context. "
                                    "Note: Only the conversation history between these two agents is shared; interactions with other agents are never included. "
                                    "Note2: Should be set to `true` only when the `prompt` lacks sufficient context and the required context exists in the conversation history.")
                },
            },
            "required": [
                "prompt"
            ]
        }
