"""
api.py — FastAPI backend exposing your existing agents/pipeline as HTTP endpoints.
Place this file in your project root, next to app.py.
"""

import io
import time
from typing import Optional, List

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pipeline import run_research_pipeline
from agents import (
    chat_with_report,
    get_followup_questions,
    chat_with_pdf,
    MODELS,
    DEFAULT_MODEL_KEY,
)
from auth.auth_logic import login_user, register_user, save_research, delete_thread
from auth.supabase_client import get_google_oauth_url, get_threads_for_user

import pdfplumber


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


app = FastAPI(title="Nexus AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten to your app's domain once deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Nexus AI API"}


# ── Request Models ────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class ResearchRequest(BaseModel):
    topic: str
    user_id: Optional[str] = None
    model_key: Optional[str] = "balanced"

class ChatMessageIn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    report: str
    topic: str
    history: List[ChatMessageIn] = []
    model_key: Optional[str] = "balanced"


# ── Models ────────────────────────────────────────────────────────────────

@app.get("/models")
def get_models():
    return {
        "models": [{"key": key, **info} for key, info in MODELS.items()],
        "default": DEFAULT_MODEL_KEY,
    }


# ── Auth ──────────────────────────────────────────────────────────────────

@app.post("/auth/login")
def login(payload: LoginRequest):
    result = login_user(payload.email, payload.password)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Login failed"))
    return result


@app.post("/auth/register")
def register(payload: RegisterRequest):
    result = register_user(payload.email, payload.password, payload.full_name)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Registration failed"))
    return result


@app.get("/auth/google-url")
def google_oauth_url():
    url = get_google_oauth_url()
    if not url:
        raise HTTPException(status_code=400, detail="Could not generate Google OAuth URL")
    return {"url": url}


# ── Research Pipeline ────────────────────────────────────────────────────

@app.post("/research")
def research(payload: ResearchRequest):
    try:
        start = time.time()
        state = run_research_pipeline(
            payload.topic,
            user_id=payload.user_id,
            model_key=payload.model_key or DEFAULT_MODEL_KEY,
        )
        elapsed = time.time() - start

        if payload.user_id:
            save_research(
                user_id=payload.user_id,
                topic=payload.topic,
                report=state.get("report", ""),
                search_results=state.get("search_results", ""),
                feedback=state.get("feedback", ""),
            )

        return {
            "topic": payload.topic,
            "report": state.get("report", ""),
            "search_results": state.get("search_results", ""),
            "scraped_content": state.get("scraped_content", ""),
            "feedback": state.get("feedback", ""),
            "elapsed": elapsed,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Chat on Report ───────────────────────────────────────────────────────

@app.post("/chat")
def chat(payload: ChatRequest):
    try:
        history = [{"role": m.role, "content": m.content} for m in payload.history]
        answer = chat_with_report(
            question=payload.question,
            report=payload.report,
            topic=payload.topic,
            history=history,
            model_key=payload.model_key or DEFAULT_MODEL_KEY,
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Follow-up Questions ──────────────────────────────────────────────────

@app.post("/followups")
def followups(topic: str, report: str, model_key: str = "balanced"):
    try:
        questions = get_followup_questions(topic, report, model_key)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── History ───────────────────────────────────────────────────────────────

@app.get("/history/{user_id}")
def get_history(user_id: str):
    try:
        threads = get_threads_for_user(user_id)
        return {"threads": threads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/history/{thread_id}")
def delete_thread_endpoint(thread_id: str):
    success = delete_thread(thread_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete thread")
    return {"success": True}


# ── PDF Upload ──────────────────────────────────────────────────────────

@app.post("/pdf/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text_from_pdf_bytes(contents)

        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            page_count = len(pdf.pages)

        return {
            "filename": file.filename,
            "text": text,
            "pages": page_count,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {e}")


# ── PDF Chat ──────────────────────────────────────────────────────────────

@app.post("/pdf/chat")
def pdf_chat(question: str, pdf_text: str, model_key: str = "balanced"):
    try:
        answer = chat_with_pdf(question=question, pdf_text=pdf_text, model_key=model_key)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)