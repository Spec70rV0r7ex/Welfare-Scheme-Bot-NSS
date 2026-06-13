# Welfare Scheme Bot (WhatsApp)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp_API-F22F46.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-4285F4.svg)

## Abstract
We developed a multilingual WhatsApp assistant powered by Gemini 3.1 Flash Lite to democratize welfare scheme awareness. Utilizing an asynchronous FastAPI backend and Twilio, the bot successfully delivers real time, hallucination free eligibility matching and localized document checklists, overcoming API latency to ensure stable, low bandwidth access for rural citizens.

## Key Features
* **Multilingual & Code-Mixed Support:** Seamlessly understands and replies in regional Indian languages, Hindi, English, and Hinglish.
* **Hallucination-Free RAG:** Grounded purely in a curated JSON catalog of verified government schemes (PM-KISAN, Ayushman Bharat, MGNREGA, PMUY).
* **Context-Aware Memory:** Maintains active chat sessions in memory, allowing for natural, multi-turn conversations without "amnesia."
* **Asynchronous Background Processing:** Employs FastAPI background tasks to prevent Twilio webhook timeouts during high AI latency.
* **Instant UX Feedback:** Immediately notifies users that it is "Searching government databases..." to provide a smooth, responsive user experience over low bandwidth.

## Tech Stack
* **Backend:** FastAPI, Python
* **LLM Engine:** Google Gemini 3.1 Flash Lite API
* **Messaging Integration:** Twilio WhatsApp Sandbox
* **Tunneling:** PyNgrok (Automated India region routing)

## Project Structure
```text
welfare-scheme-bot/
│
├── app/                        
│   ├── main.py                 # FastAPI webhook, Twilio REST client, Ngrok automation
│   ├── llm_engine.py           # Gemini API integration and in memory chat state
│   └── retrieval.py            # Knowledge base extraction and JSON parser
│
├── data/                       
│   └── raw_schemes.json        # Structured database of high impact welfare schemes
│
├── .env                        # API Keys Use your own
├── requirements.txt            # Python dependencies
└── README.md                   

```

## Local Setup & Installation

**1. Clone the repository**

```bash
git clone https://github.com/Spec70rV0r7ex/Welfare-Scheme-Bot-NSS.git
cd welfare-scheme-bot
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Add the following credentials to the `.env` file:

```env
TWILIO_ACCOUNT_SID = your_twilio_sid
TWILIO_AUTH_TOKEN = your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER = whatsapp:+14155238886
GEMINI_API_KEY = your_gemini_api_key
NGROK_AUTHTOKEN = your_ngrok_authtoken
```

**4. Run the Server**
The application is configured to automatically launch an Ngrok tunnel when the server starts.

```bash
python app/main.py
```

**5. Connect Twilio**

* Look at the terminal output to find your dynamically generated Ngrok URL (e.g., `https://xxxx.ngrok-free.app/webhook`).
* Paste this URL into your Twilio WhatsApp Sandbox settings under **"When a message comes in"**.

## Usage

1. Join the Twilio Sandbox by sending your unique join code to `+1 415 523 8886` on WhatsApp.
2. Send a natural language query in your preferred dialect (e.g., *"Mere paas zameen nahi hai, main majdoori karta hoon, mere liye kya scheme hai?"*).
3. Follow the bot's simple questions to determine your eligibility and receive a document checklist.

---

## Future Roadmap

While this prototype successfully matches citizens to schemes, our vision for scaling the platform includes:

* **Agentic AI for Auto Enrollment:** Upgrading from a conversational RAG system to an Agentic AI architecture that can securely interface with government APIs to auto fill and submit applications on the user's behalf.
* **Predictive Analytics & Big Data:** Building a data science backend (leveraging tools like PySpark for large scale processing) to provide government administrators with dashboards tracking demographic trends, identifying scheme bottlenecks, and forecasting regional resource needs.
* **Voice-First Interaction:** Integrating native Speech to Text (STT) and Text to Speech (TTS) models to fully support illiterate users, allowing them to send voice notes and receive audio guidance in their local dialects.
* **Multimodal Document Verification:** Enabling users to simply snap and send a photo of their Aadhaar card or land records directly in WhatsApp for instant, OCR based validation before they apply.
```
