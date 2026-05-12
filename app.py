import streamlit as st
from components.styles import load_styles
from components.sidebar import render_sidebar
from components.voice_input import inject_voice_listener
from components.model_selector import MODELS, DEFAULT_MODEL
from modes.research import render_research_mode
from modes.pdfchat import render_pdf_mode

# ── Page config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject voice JS listener ────────────────────────────────────────────────────
inject_voice_listener()

# ── Load all CSS ────────────────────────────────────────────────────────────────
load_styles()

# ── Session state defaults ──────────────────────────────────────────────────────
for key, default in {
    "history":               [],
    "result":                None,
    "running":               False,
    "elapsed":               0.0,
    "last_topic":            "",
    "followups":             [],
    "chat_messages":         [],
    "rag_pdf_text":          "",
    "rag_pdf_name":          "",
    "rag_messages":          [],
    "active_mode":           "research",
    "voice_topic":           "",
    "selected_model_id":     MODELS[DEFAULT_MODEL]["id"],
    "selected_model_label":  DEFAULT_MODEL,
    "selected_model_provider": "huggingface",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar (optional, for desktop) ─────────────────────────────────────────────
render_sidebar()

# ── TOP BAR — mode switcher + model selector (always visible) ───────────────────
top_left, top_right = st.columns([1, 1], gap="small")

with top_left:
    # Mode switcher
    m1, m2 = st.columns(2, gap="small")
    with m1:
        if st.button(
            "🔍 Research",
            use_container_width=True,
            type="primary" if st.session_state.active_mode == "research" else "secondary",
            key="top_research",
        ):
            st.session_state.active_mode = "research"
            st.rerun()
    with m2:
        if st.button(
            "📄 PDF Chat",
            use_container_width=True,
            type="primary" if st.session_state.active_mode == "rag" else "secondary",
            key="top_rag",
        ):
            st.session_state.active_mode = "rag"
            st.rerun()

with top_right:
    # Model selector — always visible on main page
    selected = st.selectbox(
        label="🤖 Select Model",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(
            st.session_state.get("selected_model_label", DEFAULT_MODEL)
        ),
        key="selected_model_name",
    )
    model_info = MODELS[selected]
    st.session_state["selected_model_id"]    = model_info["id"]
    st.session_state["selected_model_label"] = selected

    # Show model info badge
    st.markdown(f"""
    <div style="background:#181c24;border:1.5px solid #232838;border-radius:8px;
                padding:0.5rem 0.9rem;margin-top:0.2rem;display:flex;
                align-items:center;gap:0.6rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                     color:#4fffb0;letter-spacing:0.08em;">● {model_info['badge']}</span>
        <span style="font-size:0.72rem;color:#6b7280;">{model_info['description']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Route to correct mode ────────────────────────────────────────────────────────
if st.session_state.active_mode == "rag":
    render_pdf_mode()
else:
    render_research_mode()