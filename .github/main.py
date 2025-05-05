from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "your-openai-api-key"
GEMINI_KEY = "your-gemini-api-key"

@app.post("/chat/gpt")
async def chat_gpt(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": msg}]
    )
    reply = response["choices"][0]["message"]["content"]
    return {"reply": reply}

@app.post("/chat/gemini")
async def chat_gemini(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": msg}]}]}
    )
    result = response.json()
    reply = result["candidates"][0]["content"]["parts"][0]["text"]
    return {"reply": reply}
