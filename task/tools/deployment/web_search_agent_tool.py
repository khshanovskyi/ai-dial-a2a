from typing import Any

from aidial_sdk.chat_completion import Message

from task.tools.deployment.base import DeploymentTool
from task.tools.models import ToolCallParams
from task.utils.constants import WEB_SEARCH_AGENT_HISTORY_KEY, TOOL_CALL_HISTORY_KEY


class WebSearchAgentTool(DeploymentTool):

    @property
    def _state_key_name(self) -> str:
        return WEB_SEARCH_AGENT_HISTORY_KEY

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        msg = await super()._execute(tool_call_params)

        if msg.custom_content and msg.custom_content.state and msg.custom_content.state.get(TOOL_CALL_HISTORY_KEY):
            msg.custom_content.state = {
                WEB_SEARCH_AGENT_HISTORY_KEY: msg.custom_content.state
            }

        return msg

    @property
    def deployment_name(self) -> str:
        return "web-search-agent"

    @property
    def name(self) -> str:
        return "web_search_agent_tool"

    @property
    def description(self) -> str:
        return "Agent that performs complex search the web for current information, verify facts, and synthesize information from multiple sources"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The query or instruction to send to the WEB Search Agent."
                },
                "propagate_history": {
                    "type": "boolean",
                    "default": False,
                    "description": ("Whether to include previous conversation history between the current agent and WEB Search Agent. "
                                    "When `true`, the WEB Search Agent will have access to prior exchanges for context continuity. "
                                    "When `false`, each call starts fresh without historical context. "
                                    "Note: Only the conversation history between these two agents is shared; interactions with other agents are never included. "
                                    "Note2: Should be set to `true` only when the `prompt` lacks sufficient context and the required context exists in the conversation history.")
                },
            },
            "required": [
                "prompt"
            ]
        }
