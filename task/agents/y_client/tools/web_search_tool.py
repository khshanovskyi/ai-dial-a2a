from typing import Any

from aidial_sdk.chat_completion import Message

from task.agents.y_client.tools.base import DeploymentTool
from task.tools.models import ToolCallParams


class WebSearchTool(DeploymentTool):

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        msg = await super()._execute(tool_call_params)

        return msg

    @property
    def deployment_name(self) -> str:
        return "web-search-agent"

    @property
    def name(self) -> str:
        return "web_search_agent_tool"

    @property
    def description(self) -> str:
        return (
            "Searches the internet for current information, news, facts, and data. "
            "Returns researched findings with source citations and links. "
            "USE THIS TOOL WHEN: "
            " - User asks about current events, recent news, or time-sensitive information; "
            " - Need to verify facts, statistics, or claims that may have changed recently; "
            " - User requests research on specific topics, companies, people, or events; "
            " - Looking for latest developments, trends, or updates in any field; "
            " - Need authoritative sources or references for information. "
            "OUTPUT: Comprehensive answer with verified information and source links for user to verify."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "WEB Search request."
                }
            },
            "required": [
                "prompt"
            ]
        }