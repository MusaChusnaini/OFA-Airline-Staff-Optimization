import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

ai_model = "gemini-3.1-flash-lite"

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ada di .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(ai_model)

app = FastAPI(title="OFA Gemini Client Service")

class ChatRequest(BaseModel):
    prompt: str
    temperature: float = 0.7

@app.get("/")
def health_cek():
    return {
        "status": "OFA Gemini Client is running!",
        "engine": ai_model
    }

@app.post("/generate")
def generate_ai_response(request: ChatRequest):
    try:
        response = model.generate_content(
            request.prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=request.temperature
            )
        )
        return {
            "success": True,
            "prompt": request.prompt,
            "ai_response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))