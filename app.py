import streamlit as st
from auth.auth_ui import render_auth_page
from components.styles import load_styles
from components.sidebar import render_sidebar
from modes.research import render_research_mode
from modes.pdfchat import render_pdf_mode

# ── Page config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ─────────────────────────────────────────────────────────────────────
load_styles()

# ── Session state defaults ───────────────────────────────────────────────────────
for key, default in {
    "authenticated":        False,
    "user":                 None,
    "threads":              [],
    "active_thread":        None,
    "history":              [],
    "result":               None,
    "running":              False,
    "elapsed":              0.0,
    "last_topic":           "",
    "followups":            [],
    "chat_messages":        [],
    "rag_pdf_text":         "",
    "rag_pdf_name":         "",
    "rag_messages":         [],
    "active_mode":          "research",
    "voice_topic":          "",
    "selected_model_id":    "mistralai/Mistral-7B-Instruct-v0.3",
    "selected_model_label": "⚡ Balanced — Mistral 7B",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Auth gate ────────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    render_auth_page()
    st.stop()

# ── Sidebar ──────────────────────────────────────────────────────────────────────
render_sidebar()

# ── Top mode switcher ────────────────────────────────────────────────────────────
_c1, _c2, _c3 = st.columns([1, 2, 1])
with _c2:
    _t1, _t2 = st.columns(2, gap="small")
    with _t1:
        if st.button(
            "🔍 Research",
            use_container_width=True,
            type="primary" if st.session_state.active_mode == "research" else "secondary",
            key="top_research",
        ):
            st.session_state.active_mode = "research"
            st.rerun()
    with _t2:
        if st.button(
            "📄 PDF Chat",
            use_container_width=True,
            type="primary" if st.session_state.active_mode == "rag" else "secondary",
            key="top_rag",
        ):
            st.session_state.active_mode = "rag"
            st.rerun()

st.markdown("---")

# ── Route ────────────────────────────────────────────────────────────────────────
if st.session_state.active_mode == "rag":
    render_pdf_mode()
else:
    render_research_mode()