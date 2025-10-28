from typing import Any

from aidial_sdk.chat_completion import Message

from task.agents.y_client.tools.base import DeploymentTool
from task.tools.models import ToolCallParams


class ContentManagementTool(DeploymentTool):

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        msg = await super()._execute(tool_call_params)

        return msg

    @property
    def deployment_name(self) -> str:
        return "content-management-agent"

    @property
    def name(self) -> str:
        return "content_management_agent_tool"

    @property
    def description(self) -> str:
        return (
            "Extracts, analyzes, and answers questions from user documents (PDF, TXT, CSV, HTML). "
            "Performs both full document extraction and semantic search (RAG). "
            "USE THIS TOOL WHEN: "
            " - User uploads a document and asks questions about it; "
            " - Need to extract or read full document content; "
            " - Searching for specific information within large documents; "
            " - User asks 'what does the document say about...', 'find in the file...'; "
            " - Analyzing document content or summarizing sections. "
            "OUTPUT: Direct answers with specific references to document content. Handles pagination automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Document analysis or question request."
                }
            },
            "required": [
                "prompt"
            ]
        }