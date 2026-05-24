import streamlit as st
from auth.auth_ui import render_auth_page
from components.styles import load_styles
from modes.research import render_research_mode
from modes.pdfchat import render_pdf_mode

# ── Page config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ─────────────────────────────────────────────────────────────────────
load_styles()

# ── Session state defaults ───────────────────────────────────────────────────────
for key, default in {
    "authenticated":        False,
    "is_guest":             False,
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
    "sidebar_open":         True,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Auth gate ────────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    render_auth_page()
    st.stop()

# ── Hide native Streamlit sidebar completely ──────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.block-container { padding: 1rem 1.5rem 3rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Custom layout: left panel + main content ──────────────────────────────────────
sidebar_open = st.session_state.get("sidebar_open", True)

if sidebar_open:
    left_col, main_col = st.columns([1, 4], gap="small")
else:
    left_col, main_col = st.columns([0.001, 1], gap="small")

# ════════════════════════════════════════════════════════════════════════════════
# LEFT PANEL (custom sidebar)
# ════════════════════════════════════════════════════════════════════════════════
with left_col:
    if sidebar_open:
        from components.sidebar import render_sidebar   # FIX: was render_custom_sidebar
        render_sidebar()                                # FIX: was render_custom_sidebar()

# ════════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════════════════════
with main_col:

    # ── Top bar ───────────────────────────────────────────────────────────────
    t1, t2, t3, t4 = st.columns([0.6, 1.5, 1.5, 4], gap="small")

    with t1:
        icon = "◀" if sidebar_open else "▶"
        if st.button(icon, key="sidebar_toggle_btn",
                     use_container_width=True, help="Toggle sidebar"):
            st.session_state.sidebar_open = not sidebar_open
            st.rerun()

    with t2:
        if st.button(
            "🔍 Research", use_container_width=True,
            type="primary" if st.session_state.get("active_mode") == "research" else "secondary",
            key="top_research",
        ):
            st.session_state.active_mode = "research"
            st.rerun()

    with t3:
        if st.button(
            "📄 PDF Chat", use_container_width=True,
            type="primary" if st.session_state.get("active_mode") == "rag" else "secondary",
            key="top_rag",
        ):
            st.session_state.active_mode = "rag"
            st.rerun()

    st.markdown("---")

    # ── Route ─────────────────────────────────────────────────────────────────
    if st.session_state.get("active_mode") == "rag":
        render_pdf_mode()
    else:
        render_research_mode()