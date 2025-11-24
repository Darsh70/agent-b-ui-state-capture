from typing import Optional
from pydantic import BaseModel, Field

# The data structure the AI is required to return
class AgentAction(BaseModel):
    reasoning: str = Field(description="Brief thought process.")
    action: str = Field(description="One of: 'click', 'type', 'navigate', 'finish'")
    element_id: Optional[int] = Field(default=None, description="The numeric ID. If None, I will type blindly into the focused element.") # None for blind typing
    input_text: Optional[str] = Field(default="", description="Text to type.")
    url: Optional[str] = Field(default="", description="URL to navigate to.")