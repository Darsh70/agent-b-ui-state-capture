import os
import json
from PIL import Image
from google import genai
from google.genai import types
from schemas import AgentAction

class AIHandler:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

    def get_next_action(self, goal, history, dom_text, screenshot_path) -> AgentAction:
        image = Image.open(screenshot_path)
        prompt = f"""
        GOAL: {goal}
        HISTORY: {json.dumps(history[-3:])}
        
        ELEMENTS:
        {dom_text}

        CRITICAL INSTRUCTIONS FOR TYPING:
        1. **VISUAL FOCUS CHECK**: Look closely at the screenshot. Is the field you want to type into already highlighted (dark border), or does it have a blinking cursor?
        2. **BLIND TYPING PRIORITY**: If the correct element is ALREADY focused, DO NOT CLICK IT again. Clicking might reset focus or select the wrong parent container.
           - INSTEAD: Use action="type" with element_id=null. This types directly into the active window.
        
        INSTRUCTIONS:
        1. If a modal just opened, the input might already be focused. You can use action="type" with element_id=null.
        2. To save/create, usually press Enter after typing, or click the primary button.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AgentAction
            )
        )
        return response.parsed