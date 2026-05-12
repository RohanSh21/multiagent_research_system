import streamlit as st
import os
import requests


# ── Available models ────────────────────────────────────────────────────────────
MODELS = {
    "⚡ Balanced — Mistral 7B": {
        "id":          "mistralai/Mistral-7B-Instruct-v0.3",
        "description": "Best for general research, writing & analysis",
        "badge":       "RECOMMENDED",
        "use_case":    "General Purpose",
    },
    "🧠 Powerful — LLaMA 3 8B": {
        "id":          "meta-llama/Meta-Llama-3-8B-Instruct",
        "description": "Best for deep analysis & complex topics",
        "badge":       "ADVANCED",
        "use_case":    "Advanced Reasoning",
    },
    "🪶 Fast — Phi 2": {
        "id":          "microsoft/phi-2",
        "description": "Best for quick answers & basic questions",
        "badge":       "FASTEST",
        "use_case":    "Basic / Lightweight",
    },
    "💻 Coding — CodeLlama 7B": {
        "id":          "codellama/CodeLlama-7b-Instruct-hf",
        "description": "Best for code generation & debugging",
        "badge":       "CODING",
        "use_case":    "Code Purpose",
    },
}

DEFAULT_MODEL = "⚡ Balanced — Mistral 7B"


# ── Render selector in sidebar ──────────────────────────────────────────────────
def render_model_selector() -> None:
    """Renders model selector dropdown in sidebar."""

    st.sidebar.markdown("---")
    st.sidebar.markdown("**🤖 Select Model**")

    selected = st.sidebar.selectbox(
        label="model",
        options=list(MODELS.keys()),
        index=0,
        label_visibility="collapsed",
        key="selected_model_name",
    )

    model_info = MODELS[selected]

    st.sidebar.markdown(f"""
    <div style="background:#181c24;border:1.5px solid #232838;border-radius:10px;
                padding:0.75rem 1rem;margin-top:0.4rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#4fffb0;letter-spacing:0.08em;margin-bottom:0.3rem;">
            ● {model_info['badge']}
        </div>
        <div style="font-size:0.78rem;color:#e8eaf0;margin-bottom:0.2rem;font-weight:500;">
            {model_info['use_case']}
        </div>
        <div style="font-size:0.72rem;color:#6b7280;line-height:1.4;">
            {model_info['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Save to session state
    st.session_state["selected_model_id"]    = model_info["id"]
    st.session_state["selected_model_label"] = selected


# ── Call HuggingFace Inference API directly ─────────────────────────────────────
def _call_huggingface(prompt: str, model_id: str, temperature: float = 0.4) -> str:
    """Calls HuggingFace Inference API directly using requests — no extra package needed."""
    hf_token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")

    if not hf_token:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables.")

    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature":    max(temperature, 0.01),
            "return_full_text": False,
        },
        "options": {
            "wait_for_model": True,
        }
    }

    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()

    # Handle different response formats
    if isinstance(result, list) and len(result) > 0:
        item = result[0]
        if isinstance(item, dict):
            return item.get("generated_text", str(item))
        return str(item)
    elif isinstance(result, dict):
        return result.get("generated_text", str(result))
    return str(result)


# ── Main get_llm callable ───────────────────────────────────────────────────────
def get_llm(temperature: float = 0.4):
    """
    Returns a callable that behaves like an LLM.
    Tries HuggingFace Inference API first, falls back to Mistral.
    """

    model_id = st.session_state.get(
        "selected_model_id",
        MODELS[DEFAULT_MODEL]["id"]
    )

    class HFWrapper:
        """Wraps HuggingFace API call to look like a LangChain LLM."""
        def __init__(self, model_id, temperature):
            self.model_id    = model_id
            self.temperature = temperature

        def invoke(self, prompt: str) -> "HFWrapper":
            try:
                text = _call_huggingface(prompt, self.model_id, self.temperature)
                self.content = text
            except Exception as e:
                # Fallback to Mistral
                self.content = _mistral_fallback(prompt, self.temperature)
            return self

        @property
        def content(self):
            return self._content

        @content.setter
        def content(self, value):
            self._content = value

    return HFWrapper(model_id, temperature)


def _mistral_fallback(prompt: str, temperature: float = 0.4) -> str:
    """Fallback to Mistral via langchain_mistralai."""
    try:
        from langchain_mistralai import ChatMistralAI
        llm    = ChatMistralAI(
            model="mistral-small-latest",
            api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=temperature,
        )
        result = llm.invoke(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error: {str(e)}"