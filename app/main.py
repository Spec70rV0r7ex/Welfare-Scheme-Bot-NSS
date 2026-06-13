import os
from fastapi import FastAPI, Form, Response, BackgroundTasks
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from llm_engine import generate_bot_response 

load_dotenv()
app = FastAPI()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

twilio_client = Client(account_sid, auth_token)

def process_and_reply(user_phone: str, user_message: str):
    print("Background: Asking Gemini...")
    try:
        twilio_client.messages.create(
            from_ = twilio_number,
            body = "⏳ _Searching government databases for schemes..._",
            to = user_phone
        )

        bot_reply = generate_bot_response(user_phone=user_phone, user_message=user_message)
        print("Background: Gemini finished! Pushing to WhatsApp...")

        if not user_phone.startswith("whatsapp:"):
            user_phone = f"whatsapp:{user_phone}"
        twilio_client.messages.create(
            from_ = twilio_number,
            body = bot_reply,
            to = user_phone
        )
        print("Message successfully delivered!")
        
    except Exception as e:
        print(f"Background Error: {e}")

        if not user_phone.startswith("whatsapp:"):
            user_phone = f"whatsapp:{user_phone}"
            
        twilio_client.messages.create(
            from_ = twilio_number,
            body = "Maaf karein, network error. Kripya thodi der baad prayas karein.",
            to = user_phone
        )

@app.post("/webhook")
def receive_message(
    background_tasks: BackgroundTasks,
    Body: str = Form(...),
    From: str = Form(...)
):
    user_phone = From       
    user_message = Body.strip()

    print(f"\nFAST RECEIVE [{user_phone}]: {user_message}")
    
    background_tasks.add_task(process_and_reply, user_phone, user_message)

    empty_response = MessagingResponse()
    return Response(content = str(empty_response), media_type = "application/xml")

if __name__ == "__main__":
    import uvicorn
    from pyngrok import ngrok, conf

    ngrok_token = os.getenv("NGROK_AUTHTOKEN")
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
        pyngrok_config = conf.PyngrokConfig(region = "in")
        public_url = ngrok.connect(8000, pyngrok_config = pyngrok_config).public_url # type: ignore
        print("NGROK TUNNEL (BACKGROUND MODE) STARTED!")
        print(f"URL: {public_url}/webhook")

    uvicorn.run(app, host = "0.0.0.0", port = 8000)
