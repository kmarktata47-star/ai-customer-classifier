from typing import Literal
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()
client = genai.Client()

MODEL = "gemini-3.5-flash-lite"


class Ticket(BaseModel):
    category: Literal[
        "Payment Issue",
        "Technical Problem",
        "Account Access",
        "Shipping/Delivery",
        "Refund Request",
        "General Inquiry",
    ]
    urgency: Literal["Low", "Medium", "High"]
    reason: str


SYSTEM_PROMPT = """You are a customer support triage assistant.
Classify the customer's message into a category and an urgency level.
High urgency = money lost, account locked, or service completely broken.
Medium urgency = something is not working but there is a workaround.
Low urgency = questions or feedback with no time pressure.
Keep 'reason' to one short sentence."""


def classify(message):
    response = client.models.generate_content(
        model=MODEL,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=Ticket,
        ),
    )
    return response.parsed


if __name__ == "__main__":
    result = classify("Great service, thank you!")
    print("Category:", result.category)
    print("Urgency:", result.urgency)
    print("Reason:", result.reason)