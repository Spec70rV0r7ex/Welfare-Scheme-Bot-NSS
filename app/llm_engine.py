import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from retrieval import get_knowledge_context

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = gemini_key)
knowledge_base = get_knowledge_context()

SYSTEM_INSTRUCTION = f"""
You are an empathetic, expert rural social worker assistant helping citizens discover government welfare schemes. 
You communicate seamlessly in Indian languages, handling code mixing (e.g., Hinglish, Tamlish, Benglish) dynamically based on how the user talks.

Here is your official, ground truth database of available schemes:
{knowledge_base}

STRICT PROTOCOLS:
1. Grounding: You ONLY recommend or discuss schemes listed in the context above. If a user asks about a scheme not listed, politely state you do not have verified information on it. DO NOT hallucinate rules.
2. Conversation Flow: Keep interactions short and concise (under 3 sentences per turn) because the user is on WhatsApp and a low bandwidth.
3. Eligibility Gathering: Ask 1 simple question at a time to determine eligibility (e.g., occupation, income, land ownership). Do not overwhelm them.
4. Language: Always reply in the same blend of language/dialect the user used.
5. Final Checklist: If they qualify for a scheme, state it clearly and provide a neat bulleted list of the exact documents required based ONLY on the database.
"""

def generate_bot_response(user_phone: str, user_message: str, chat_history: list = None) -> str: # type: ignore
    formatted_contents = []
    if chat_history:
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(types.Content(role = role, parts = [types.Part.from_text(text = msg["text"])]))
    formatted_contents.append(types.Content(role = "user", parts = [types.Part.from_text(text = user_message)]))

    try:
        response = client.models.generate_content(
            model = 'gemini-3.1-flash-lite',
            contents = formatted_contents,
            config = types.GenerateContentConfig(
                system_instruction = SYSTEM_INSTRUCTION,
                temperature = 0.3,
            )
        )
        return response.text # type: ignore
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I am experiencing a temporary connection issue. Please try again in a moment."
