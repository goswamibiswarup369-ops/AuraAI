# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# YOUR API KEY (loaded securely from .env — never hardcode this)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class Action(BaseModel):
    feature: str
                                                #  Website run:-  uvicorn app:app --reload
    context: str
    role: str
    settings: dict

def get_live_chat_model():
    """Live-scans your account for the newest working model to avoid 'decommissioned' errors."""
    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        resp = requests.get(url, headers=headers).json()

        # Get all IDs and filter out safety/audio/vision models
        all_ids = [m['id'] for m in resp.get('data', [])]
        valid_chat_models = [m for m in all_ids if
                             ('/' not in m) and
                             not any(x in m.lower() for x in ['guard', 'vision', 'whisper', 'audio'])]

        # Sort to get the most recent model (usually latest version number)
        valid_chat_models.sort(reverse=True)
        return valid_chat_models[0] if valid_chat_models else "llama-3.1-8b-instant"
    except:
        return "llama-3.1-8b-instant"  # Safe fallback

@app.post("/feature")
async def handle_feature(data: Action):
    # This automatically finds a working model so the 'choices' error disappears
    model = get_live_chat_model()
    print(f">> AURA ENGINE START: {model} | ROLE: {data.role}")

    role_prompts = {
        "student": "Expert Academic Mentor. Focus on study tips and simplicity.",
        "teacher": "Curriculum Specialist. Focus on lesson plans and pedagogy.",
        "faculty": "Academic Strategist. Focus on research and university operations."
    }

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"You are Aura AI. Role: {role_prompts.get(data.role)}. Depth: {data.settings.get('depth')}"},
            {"role": "user", "content": f"Execute {data.feature} for: {data.context}"}
        ],
        "temperature": float(data.settings.get("temp", 0.5))
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        res = r.json()
        if "choices" in res:
            return {"result": res["choices"][0]["message"]["content"], "model": model}
        # If model name is wrong, we report the actual Groq error
        error_msg = res.get("error", {}).get("message", "Model Access Error")
        return {"result": f"Aura System Alert: {error_msg}."}
    except Exception as e:
        return {"result": f"Connection Error: {str(e)}"}