import streamlit as st
from components.styles import load_styles
from components.sidebar import render_sidebar
from components.voice_input import inject_voice_listener
from modes.research import render_research_mode
from modes.pdfchat import render_pdf_mode

# ── Page config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject voice JS listener ────────────────────────────────────────────────────
inject_voice_listener()

# ── Load all CSS ────────────────────────────────────────────────────────────────
load_styles()

# ── Session state defaults ──────────────────────────────────────────────────────
for key, default in {
    "history":        [],
    "result":         None,
    "running":        False,
    "elapsed":        0.0,
    "last_topic":     "",
    "followups":      [],
    "chat_messages":  [],
    "rag_pdf_text":   "",
    "rag_pdf_name":   "",
    "rag_messages":   [],
    "active_mode":    "research",
    "voice_topic":    "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ─────────────────────────────────────────────────────────────────────
render_sidebar()

# ── Top mode switcher (mobile friendly) ─────────────────────────────────────────
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

# ── Route to correct mode ────────────────────────────────────────────────────────
if st.session_state.active_mode == "rag":
    render_pdf_mode()
else:
    render_research_mode()