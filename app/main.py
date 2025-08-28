from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
from groq import Groq
import os
from dotenv import load_dotenv
import pathlib
import json

# Message models
class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    history: List[Message]

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Create FastAPI instance
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load system prompt
PROMPT_FILE = pathlib.Path(__file__).parent.parent / "Prompts" / "gold_assistant.system.md"
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

SIMPLIFY_URL = "https://www.simplifymoney.in/"

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Build message list for Groq
        messages_for_groq = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages_for_groq += [{"role": m.role, "content": m.content} for m in request.history]

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages_for_groq
        )

        ai_response = response.choices[0].message.content
        if not ai_response:
            ai_response = "⚠️ AI returned empty response"
        
        print("AI Response:", ai_response)
        # Attempt to parse JSON returned by prompt
        try:
            parsed = json.loads(ai_response)
        except json.JSONDecodeError:
            # Fallback: check if it's a plain string response
            parsed = {"answer": ai_response, "action": None, "slots": {}, "follow_up": None}

        # Force redirect if confirmed purchase
        answer_text = parsed.get("answer", "").lower()
        if parsed.get("action") == "CALL_PURCHASE_API" or "purchase of" in answer_text or "transaction" in answer_text or "confirmed" in answer_text:
            parsed["redirect_url"] = SIMPLIFY_URL

        # Build response for frontend
        resp = {"answer": parsed.get("answer", "⚠️ AI returned no answer")}
        if "redirect_url" in parsed:
            resp["redirect_url"] = parsed["redirect_url"]

        return resp



    except Exception as e:
        return {"answer": f"⚠️ Error occurred: {str(e)}"}
