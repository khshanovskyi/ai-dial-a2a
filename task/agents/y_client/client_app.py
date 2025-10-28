import uvicorn
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from task.agents.y_client.client_agent import ClientAgent
from task.agents.y_client.tools.calculations_tool import CalculationsTool
from task.agents.y_client.tools.content_management_tool import ContentManagementTool
from task.agents.y_client.tools.web_search_tool import WebSearchTool
from task.tools.base_tool import BaseTool
from task.utils.constants import DIAL_ENDPOINT, DEPLOYMENT_NAME


class ClientApplication(ChatCompletion):

    def __init__(self):
        self.tools: list[BaseTool] = [
            CalculationsTool(DIAL_ENDPOINT),
            ContentManagementTool(DIAL_ENDPOINT),
            WebSearchTool(DIAL_ENDPOINT),
        ]

    async def chat_completion(self, request: Request, response: Response) -> None:
        with response.create_single_choice() as choice:
            await ClientAgent(
                endpoint=DIAL_ENDPOINT,
                tools=self.tools
            ).handle_request(
                choice=choice,
                deployment_name=DEPLOYMENT_NAME,
                request=request,
                response=response,
            )


app: DIALApp = DIALApp()
agent_app = ClientApplication()
app.add_chat_completion(deployment_name="client-agent", impl=agent_app)

if __name__ == "__main__":
    uvicorn.run(app, port=5005, host="0.0.0.0")
