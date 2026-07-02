import logging
from enum import Enum

from google import genai
from google.genai.types import GenerateContentConfig

import config
import prompts

client = genai.Client(api_key=config.GEMINI_API_KEY)

class ToastDecision(Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"

GLOBAL_CONFIG = GenerateContentConfig(
    system_instruction=prompts.SYSTEM_PROMPT,
    response_mime_type="text/x.enum",
    response_schema=ToastDecision,
    temperature=0.0
)

async def evaluate_for_toast(text: str) -> bool:
    """Sends text to Gemini and returns True if it deserves a toast, False otherwise."""
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=text,
            config=GLOBAL_CONFIG
        )

        return response.text == ToastDecision.TRUE.value

    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        return False