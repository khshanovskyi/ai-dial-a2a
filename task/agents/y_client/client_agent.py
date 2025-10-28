from task.agents.base_agent import BaseAgent
from task.agents.y_client._prompts import SYSTEM_PROMPT
from task.tools.base_tool import BaseTool


class ClientAgent(BaseAgent):

    def __init__(self, endpoint: str, tools: list[BaseTool]):
        super().__init__(
            endpoint = endpoint,
            tools = tools,
            system_prompt=SYSTEM_PROMPT
        )

