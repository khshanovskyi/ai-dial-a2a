from typing import Any

from aidial_sdk.chat_completion import Message

from task.tools.deployment.base_agent_tool import BaseAgentTool
from task.tools.models import ToolCallParams
from task.utils.constants import CALCULATIONS_AGENT_HISTORY_KEY, TOOL_CALL_HISTORY_KEY


class CalculationsAgentTool(BaseAgentTool):

    @property
    def _state_key_name(self) -> str:
        return CALCULATIONS_AGENT_HISTORY_KEY

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        msg = await super()._execute(tool_call_params)

        if msg.custom_content and msg.custom_content.state and msg.custom_content.state.get(TOOL_CALL_HISTORY_KEY):
            msg.custom_content.state = {
                CALCULATIONS_AGENT_HISTORY_KEY: msg.custom_content.state
            }

        return msg

    @property
    def deployment_name(self) -> str:
        return "calculations-agent"

    @property
    def name(self) -> str:
        return "calculations_agent_tool"

    @property
    def description(self) -> str:
        return "Agent that performs calculations, can run Python code with Python Code Interpreter tool, generate chart bars from some data"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The query or instruction to send to the Calculations Agent."
                },
                "propagate_history": {
                    "type": "boolean",
                    "default": False,
                    "description": ("Whether to include previous conversation history between the current agent and Calculations Agent. "
                                    "When `true`, the Calculations Agent will have access to prior exchanges for context continuity. "
                                    "When `false`, each call starts fresh without historical context. "
                                    "Note: Only the conversation history between these two agents is shared; interactions with other agents are never included. "
                                    "Note2: Should be set to `true` only when the `prompt` lacks sufficient context and the required context exists in the conversation history.")
                },
            },
            "required": [
                "prompt"
            ]
        }
