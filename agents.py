from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from tools import web_search, scrape_url
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Fixed model for tool-calling agents (search + reader need function calling)
llm = ChatMistralAI(model="mistral-small-2506", temperature=0)

def build_search_agent():
    return create_agent(model=llm, tools=[web_search])

def build_reader_agent():
    return create_agent(model=llm, tools=[scrape_url])


# ── Selectable models (writer / critic / chat / PDF chat only) ─────────────
MODELS = {
    "balanced": {
        "label": "⚡ Balanced — Mistral 7B",
        "id": "mistralai/Mistral-7B-Instruct-v0.3",
        "description": "Best for general research, writing & analysis",
        "badge": "RECOMMENDED",
        "use_case": "General Purpose",
    },
    "advanced": {
        "label": "🧠 Powerful — LLaMA 3 8B",
        "id": "meta-llama/Meta-Llama-3-8B-Instruct",
        "description": "Best for deep analysis & complex topics",
        "badge": "ADVANCED",
        "use_case": "Advanced Reasoning",
    },
    "fast": {
        "label": "🪶 Fast — Phi 2",
        "id": "microsoft/phi-2",
        "description": "Best for quick answers & basic questions",
        "badge": "FASTEST",
        "use_case": "Basic / Lightweight",
    },
    "coding": {
        "label": "💻 Coding — CodeLlama 7B",
        "id": "codellama/CodeLlama-7b-Instruct-hf",
        "description": "Best for code generation & debugging",
        "badge": "CODING",
        "use_case": "Code Purpose",
    },
}
DEFAULT_MODEL_KEY = "balanced"


def _call_huggingface(prompt: str, model_id: str, temperature: float = 0.4) -> str:
    hf_token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables.")

    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 800,
            "temperature": max(temperature, 0.01),
            "return_full_text": False,
        },
        "options": {"wait_for_model": True},
    }
    response = requests.post(api_url, headers=headers, json=payload, timeout=90)
    response.raise_for_status()
    result = response.json()

    if isinstance(result, list) and result:
        item = result[0]
        return item.get("generated_text", str(item)) if isinstance(item, dict) else str(item)
    elif isinstance(result, dict):
        return result.get("generated_text", str(result))
    return str(result)


def _mistral_fallback(prompt: str, temperature: float = 0.4) -> str:
    fallback_llm = ChatMistralAI(model="mistral-small-2506", temperature=temperature)
    result = fallback_llm.invoke(prompt)
    return result.content if hasattr(result, "content") else str(result)


def call_selected_llm(prompt: str, model_key: str = DEFAULT_MODEL_KEY, temperature: float = 0.4) -> str:
    """Routes text-generation calls to the user's selected model. Falls back to Mistral on failure."""
    model_info = MODELS.get(model_key, MODELS[DEFAULT_MODEL_KEY])
    model_id = model_info["id"]

    # "Balanced" model is Mistral-branded but we actually run it via native Mistral API for reliability
    if model_key == "balanced":
        try:
            return _mistral_fallback(prompt, temperature)
        except Exception as e:
            return f"Error calling model: {e}"

    try:
        return _call_huggingface(prompt, model_id, temperature)
    except Exception:
        # HF model unavailable/rate-limited — fall back so the user still gets a response
        return _mistral_fallback(prompt, temperature)


# ── Writer ────────────────────────────────────────────────────────────────
def write_report(topic: str, research: str, model_key: str = DEFAULT_MODEL_KEY) -> str:
    prompt = f"""You are an expert research writer. Write clear, structured and insightful reports.

Write a detailed research report on the topic below.
Topic: {topic}
Research Gathered: {research}

Structure the report as:
--Introduction
--Key Findings (minimum 3 well explained points)
--Conclusion
--Sources (list all urls found in the research)

Be detailed, factual and professional."""
    return call_selected_llm(prompt, model_key)


# ── Critic ────────────────────────────────────────────────────────────────
def critique_report(report: str, model_key: str = DEFAULT_MODEL_KEY) -> str:
    prompt = f"""You are a sharp and constructive research critic. Be honest and specific.

Review the research report below and evaluate it strictly.
Report: {report}

Respond in this exact format:
score:x/10

strengths:
-...
-...
areas to improve:
-...
-...
one line verdict:
..."""
    return call_selected_llm(prompt, model_key)


# ── Chat with report ─────────────────────────────────────────────────────
def chat_with_report(question: str, report: str, topic: str, history: list,
                      model_key: str = DEFAULT_MODEL_KEY) -> str:
    history_text = "\n".join(f"{m['role']}: {m['content']}" for m in history) if history else "(no previous messages)"
    prompt = f"""You are a helpful research assistant. Answer questions about the report below using only information from it. If the answer isn't in the report, say so honestly.

Topic: {topic}

Report:
{report}

Conversation so far:
{history_text}

Question: {question}"""
    return call_selected_llm(prompt, model_key)


# ── Follow-up questions ──────────────────────────────────────────────────
def get_followup_questions(topic: str, report: str, model_key: str = DEFAULT_MODEL_KEY) -> list:
    prompt = f"""You suggest insightful follow-up questions a reader might ask after reading a research report. Return exactly 4 questions, one per line, no numbering, no extra text.

Topic: {topic}

Report excerpt:
{report}"""
    raw = call_selected_llm(prompt, model_key)
    questions = [q.strip("-• \t") for q in raw.split("\n") if q.strip()]
    return questions[:4]


# ── Chat with PDF ─────────────────────────────────────────────────────────
def chat_with_pdf(question: str, pdf_text: str, model_key: str = DEFAULT_MODEL_KEY) -> str:
    prompt = f"""You are a helpful assistant answering questions about an uploaded PDF document. Use only the document content below. If the answer isn't in the document, say so honestly.

Document content:
{pdf_text[:6000]}

Question: {question}"""
    return call_selected_llm(prompt, model_key)