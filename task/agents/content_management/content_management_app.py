import uvicorn
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from task.agents.content_management.content_management_agent import ContentManagementAgent
from task.agents.content_management.tools.files.file_content_extraction_tool import FileContentExtractionTool
from task.agents.content_management.tools.rag.document_cache import DocumentCache
from task.agents.content_management.tools.rag.rag_tool import RagTool
from task.tools.base_tool import BaseTool
from task.tools.deployment.calculations_agent_tool import CalculationsAgentTool
from task.tools.deployment.web_search_agent_tool import WebSearchAgentTool
from task.utils.constants import DIAL_ENDPOINT, DEPLOYMENT_NAME

#TODO:
# 1. Create ContentManagementApplication class and extend ChatCompletion
# 2. As a tools for ContentManagementAgent you need to provide:
#   - FileContentExtractionTool
#   - RagTool
#   - CalculationsAgentTool (MAS Mesh)
#   - WebSearchAgentTool (MAS Mesh)
# 3. Override the chat_completion method of ChatCompletion, create Choice and call ContentManagementAgent
# ---
# 4. Create DIALApp with deployment_name `content-managemen-agent` (the same as in the core config) and impl is instance
#    of the ContentManagementApplication
# 5. Add starter with DIALApp, port is 5002 (see core config)

raise NotImplementedError()
