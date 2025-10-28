from typing import Any

from aidial_sdk.chat_completion import Message

from task.agents.y_client.tools.base import DeploymentTool
from task.tools.models import ToolCallParams


class CalculationsTool(DeploymentTool):

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        msg = await super()._execute(tool_call_params)

        return msg

    @property
    def deployment_name(self) -> str:
        return "calculations-agent"

    @property
    def name(self) -> str:
        return "calculations_agent_tool"

    @property
    def description(self) -> str:
        return (
            "Performs mathematical calculations, data analysis, and Python code execution. "
            "Handles both simple arithmetic and complex computational tasks. "
            "USE THIS TOOL WHEN: "
            " - User needs mathematical calculations (arithmetic, algebra, statistics); "
            " - Data analysis, processing, or visualization required; "
            " - Scientific computing with numpy, pandas, matplotlib, scipy; "
            " - Multi-step calculations or algorithms; "
            " - Need to generate charts, plots, or data files. "
            "OUTPUT: Calculation results with step-by-step breakdown when complex. Can generate and return files."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Calculation or data analysis request."
                }
            },
            "required": [
                "prompt"
            ]
        }