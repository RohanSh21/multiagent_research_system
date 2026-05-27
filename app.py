import streamlit as st
from auth.auth_ui import render_auth_page
from components.styles import load_styles
from modes.research import render_research_mode
from modes.pdfchat import render_pdf_mode

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexus AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_styles()

# ── Session defaults ──────────────────────────────────────────────────────────
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

# ── Auth gate ─────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated", False):
    render_auth_page()
    st.stop()

# ── Hide native Streamlit sidebar ─────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.block-container { padding: 1rem 1.5rem 3rem !important; max-width: 100% !important; }
.mobile-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.65); z-index: 998;
    backdrop-filter: blur(3px);
}
.mobile-overlay.open { display: block; }
@media (max-width: 1024px) {
    .rm-drawer {
        position: fixed; top: 0; left: 0; bottom: 0;
        width: 280px; background: #0a0a0a;
        border-right: 1px solid #262626;
        z-index: 999; overflow-y: auto; padding: 1rem 0.75rem;
        transform: translateX(-280px);
        transition: transform 0.22s cubic-bezier(0.4,0,0.2,1);
    }
    .rm-drawer.open { transform: translateX(0); }
}
@media (min-width: 1025px) {
    .rm-drawer { display: none !important; }
}
</style>
<div class="mobile-overlay" id="mobileOverlay" onclick="closeSidebar()"></div>
<div class="rm-drawer" id="rmDrawer"></div>
<script>
function openSidebar() {
    document.getElementById('rmDrawer').classList.add('open');
    document.getElementById('mobileOverlay').classList.add('open');
}
function closeSidebar() {
    document.getElementById('rmDrawer').classList.remove('open');
    document.getElementById('mobileOverlay').classList.remove('open');
}
function toggleSidebar() {
    const open = document.getElementById('rmDrawer').classList.contains('open');
    open ? closeSidebar() : openSidebar();
}
window.addEventListener('resize', () => {
    if (window.innerWidth > 1024) closeSidebar();
});
</script>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
sidebar_open = st.session_state.get("sidebar_open", True)
active_mode  = st.session_state.get("active_mode", "research")

if sidebar_open:
    left_col, main_col = st.columns([1, 4], gap="small")
else:
    left_col, main_col = st.columns([0.001, 1], gap="small")

# ── Sidebar column (desktop) ──────────────────────────────────────────────────
with left_col:
    if sidebar_open:
        from components.sidebar import render_sidebar
        render_sidebar()

# ── Main content column ───────────────────────────────────────────────────────
with main_col:

    # Top bar — only sidebar toggle, no mode buttons
    c1, _ = st.columns([0.4, 5], gap="small")
    with c1:
        label = "◀" if sidebar_open else "▶"
        if st.button(label, key="sidebar_toggle_btn",
                     use_container_width=True, help="Toggle sidebar"):
            st.session_state.sidebar_open = not sidebar_open
            st.rerun()

    st.markdown("---")

    # Route
    if active_mode == "rag":
        render_pdf_mode()
    else:
        render_research_mode()