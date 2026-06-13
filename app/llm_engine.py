import os
from dotenv import load_dotenv
from google import genai
from retrieval import get_knowledge_context

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    print("🚨 FATAL ERROR: GEMINI_API_KEY not found!")

client = genai.Client(api_key = gemini_key)
knowledge_base = get_knowledge_context()

SYSTEM_INSTRUCTION = f"""
You are an empathetic, expert rural social worker assistant helping citizens discover government welfare schemes. 
You communicate seamlessly in Indian languages, handling code-mixing (e.g., Hinglish, Tamlish, Benglish) dynamically based on how the user talks.

Here is your official, ground-truth database of available schemes:
{knowledge_base}

STRICT PROTOCOLS:
1. Grounding: You ONLY recommend or discuss schemes listed in the context above.
2. Conversation Flow: Keep interactions short and concise.
3. Eligibility Gathering: Ask ONE simple question at a time.
4. Language: Always reply in the same blend of language/dialect the user used.
5. Final Checklist: If they qualify, state it clearly and provide a neat bulleted list of the exact documents required.
"""

active_chats = {}

def generate_bot_response(user_phone: str, user_message: str):
    try:
        if user_phone not in active_chats:
            active_chats[user_phone] = client.chats.create(
                model = 'gemini-3.1-flash-lite',
                config = genai.types.GenerateContentConfig(
                    system_instruction = SYSTEM_INSTRUCTION,
                    temperature = 0.3,
                )
            )

        response = active_chats[user_phone].send_message(user_message)
        return response.text
        
    except Exception as e:
        print(f"🚨 GEMINI API ERROR: {e}")
        return "Sorry, network error. Please try again."
