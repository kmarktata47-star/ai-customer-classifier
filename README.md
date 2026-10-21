# AI Customer Classifier

A small web app that reads a customer support message and classifies it by category and urgency using the Gemini API.

## How it works
1. The user types a customer message in a Streamlit page.
2. The message is sent to a Gemini model with instructions for support triage.
3. The model replies in a fixed structure (category, urgency, reason), defined with Pydantic.
4. The page shows the result.

## Run it yourself
1. Install the packages: `pip install google-genai streamlit pydantic python-dotenv`
2. Get a free API key at https://aistudio.google.com/apikey
3. Create a file named `.env` containing: `GEMINI_API_KEY=your-key-here`
4. Start the app: `python -m streamlit run app.py`

## Status
Version 1. Next steps: process CSV files and measure accuracy against labeled examples.