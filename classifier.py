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

Category rules:
- Classify by the topic of the message, even when it is a simple question. Questions about payment methods, fees or invoices are Payment Issue. Questions about logging in or changing account details are Account Access. Questions about delivery, tracking or shipping times are Shipping/Delivery.
- Refund Request is for any message whose main goal is to get money back.
- Use General Inquiry only when nothing else fits: opening hours, discounts, praise, feedback, feature suggestions, policies, or unclear text.

Urgency rules:
- High: the customer is blocked from using the service or their account, or is losing money right now (for example a double charge).
- Medium: there is a real problem or a request that needs action soon, but the customer is not blocked and no money is being lost right now. Refund requests, damaged or wrong items, and changes to recent orders are usually Medium.
- Low: simple questions, feedback, and requests with no time pressure.

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