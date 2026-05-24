import streamlit as st
from auth.auth_ui import render_auth_page
from components.styles import load_styles
from modes.research import render_research_mode
from modes.pdfchat import render_pdf_mode

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
load_styles()

# ── Session state defaults ────────────────────────────────────────────────────
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

# ── Determine sidebar state ───────────────────────────────────────────────────
sidebar_open = st.session_state.get("sidebar_open", True)

# ── Inject full-page HTML scaffold ───────────────────────────────────────────
# This creates the fixed sidebar drawer + main content wrapper that CSS targets.
# The actual Streamlit widgets rendered below will flow into .rm-content naturally
# because Streamlit renders sequentially into the page body.
sidebar_class = "rm-sidebar open" if sidebar_open else "rm-sidebar"
main_class    = "rm-main" if sidebar_open else "rm-main full-width"
active_mode   = st.session_state.get("active_mode", "research")

st.markdown(f"""
<!-- Dark overlay for mobile drawer -->
<div class="mobile-overlay" id="mobileOverlay" onclick="closeSidebar()"></div>

<!-- Fixed sidebar scaffold (Streamlit widgets injected inside via column trick) -->
<div class="{sidebar_class}" id="rmSidebar"></div>

<!-- Main wrapper open tag -->
<div class="{main_class}" id="rmMain">

  <!-- Top bar -->
  <div class="rm-topbar">
    <button class="rm-topbar-icon" onclick="toggleSidebar()" title="Toggle sidebar" id="menuBtn">☰</button>
    <span class="rm-topbar-title">🧠 ResearchMind</span>
  </div>

</div>

<script>
function toggleSidebar() {{
    const sb = document.getElementById('rmSidebar');
    const main = document.getElementById('rmMain');
    const overlay = document.getElementById('mobileOverlay');
    const isMobile = window.innerWidth <= 1024;
    if (isMobile) {{
        const isOpen = sb.classList.contains('open');
        if (isOpen) {{
            sb.classList.remove('open');
            overlay.classList.remove('open');
        }} else {{
            sb.classList.add('open');
            overlay.classList.add('open');
        }}
    }} else {{
        // desktop: toggle sidebar + main margin via Streamlit rerun
        window._streamlitToggle && window._streamlitToggle();
    }}
}}
function closeSidebar() {{
    document.getElementById('rmSidebar').classList.remove('open');
    document.getElementById('mobileOverlay').classList.remove('open');
}}
// On resize, reset overlay if switching back to desktop
window.addEventListener('resize', function() {{
    if (window.innerWidth > 1024) {{
        document.getElementById('mobileOverlay').classList.remove('open');
    }}
}});
</script>
""", unsafe_allow_html=True)

# ── Layout: sidebar column + main column ─────────────────────────────────────
# On desktop: [1, 4] ratio. On tablet/mobile: CSS hides left col, drawer takes over.
if sidebar_open:
    left_col, main_col = st.columns([1, 4], gap="small")
else:
    left_col, main_col = st.columns([0.001, 1], gap="small")

# ── LEFT PANEL — sidebar content ─────────────────────────────────────────────
with left_col:
    if sidebar_open:
        from components.sidebar import render_sidebar
        render_sidebar()

# ── RIGHT PANEL — main content ────────────────────────────────────────────────
with main_col:

    # Top bar Streamlit buttons (mode switcher + desktop toggle)
    tb1, tb2, tb3, tb4 = st.columns([0.5, 1.5, 1.5, 4], gap="small")

    with tb1:
        # Desktop sidebar toggle (rerun-based)
        icon = "◀" if sidebar_open else "▶"
        if st.button(icon, key="sidebar_toggle_btn",
                     use_container_width=True, help="Toggle sidebar"):
            st.session_state.sidebar_open = not sidebar_open
            st.rerun()

    with tb2:
        if st.button(
            "🔍 Research", use_container_width=True,
            type="primary" if active_mode == "research" else "secondary",
            key="top_research",
        ):
            st.session_state.active_mode = "research"
            st.rerun()

    with tb3:
        if st.button(
            "📄 PDF Chat", use_container_width=True,
            type="primary" if active_mode == "rag" else "secondary",
            key="top_rag",
        ):
            st.session_state.active_mode = "rag"
            st.rerun()

    st.markdown("---")

    # ── Route ─────────────────────────────────────────────────────────
    if active_mode == "rag":
        render_pdf_mode()
    else:
        render_research_mode()