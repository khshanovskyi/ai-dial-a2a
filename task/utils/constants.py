import os

DIAL_ENDPOINT = os.getenv('DIAL_ENDPOINT', "http://localhost:8080")
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME', 'gpt-4o')

TOOL_CALL_HISTORY_KEY = "tool_call_history"
CUSTOM_CONTENT = "custom_content"

WEB_SEARCH_AGENT_HISTORY_KEY = "web_search_agent_history"
CONTENT_MANAGEMENT_AGENT_HISTORY_KEY = "content_management_agent_history"
CALCULATIONS_AGENT_HISTORY_KEY = "calculations_agent_history"