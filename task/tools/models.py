from dataclasses import dataclass
from typing import Optional

from aidial_sdk.chat_completion import Choice, Stage, ToolCall, Message

@dataclass
class ToolCallParams:
    tool_call: ToolCall
    stage: Stage
    choice: Choice
    api_key: str
    conversation_id: str
    messages: list[Message] = list


@dataclass
class ToolStageConfig:
    create_stage: bool = True
    show_request_in_stage: bool = True
    show_response_in_stage: bool = True
    stage_name: Optional[str] = None
