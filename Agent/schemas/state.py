from typing import Optional
from typing_extensions import Annotated,TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    page_content:list[str]
    page_image_prompts: list[str]
    page_image_url: Optional[list[str]]
    messages: Annotated[list,add_messages]