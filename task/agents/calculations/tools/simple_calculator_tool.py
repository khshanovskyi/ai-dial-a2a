import json
from typing import Any

from aidial_sdk.chat_completion import Message

from task.tools.base_tool import BaseTool
from task.tools.models import ToolCallParams


class SimpleCalculatorTool(BaseTool):

    @property
    def name(self) -> str:
        return "simple_calculator_tool"

    @property
    def description(self) -> str:
        return "Performs simple math calculations."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "First operand"
                },
                "b": {
                    "type": "integer",
                    "description": "Second operand"
                },
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Mathematical operation to perform"
                }
            },
            "required": ["a", "b", "operation"]
        }

    async def _execute(self, tool_call_params: ToolCallParams) -> str | Message:
        arguments = json.loads(tool_call_params.tool_call.function.arguments)
        a = arguments["a"]
        b = arguments["b"]
        operation = arguments["operation"]

        tool_call_params.stage.append_name(f": {a} {operation} {b}")

        if operation == "add":
            return a + b
        if operation == "subtract":
            return a - b
        if operation == "multiply":
            return a * b
        if operation == "divide":
            return a / b

        raise RuntimeError(f"Unknown operation: {operation}")


