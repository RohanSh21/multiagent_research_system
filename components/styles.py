import streamlit as st


def load_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:           #0f0f0f;
        --surface:      #161616;
        --surface2:     #1e1e1e;
        --surface3:     #252525;
        --border:       #2a2a2a;
        --border2:      #333333;
        --accent:       #2563eb;
        --accent-hover: #1d4ed8;
        --accent-soft:  rgba(37,99,235,0.12);
        --green:        #10b981;
        --green-soft:   rgba(16,185,129,0.12);
        --text:         #ececec;
        --text2:        #a0a0a0;
        --text3:        #666666;
        --danger:       #ef4444;
        --danger-soft:  rgba(239,68,68,0.12);
        --radius:       12px;
        --radius-lg:    18px;
        --sidebar-w:    260px;
        --topbar-h:     52px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg);
        color: var(--text);
        -webkit-font-smoothing: antialiased;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Hide native Streamlit sidebar & collapse control */
    [data-testid="stSidebar"]       { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Full-width, zero padding — we control layout ourselves */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 99px; }

    /* ═══════════════════════════════════════════════════
       MOBILE DRAWER OVERLAY
    ═══════════════════════════════════════════════════ */
    .mobile-overlay {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.6);
        z-index: 998;
        backdrop-filter: blur(2px);
    }
    .mobile-overlay.open { display: block; }

    /* ═══════════════════════════════════════════════════
       CUSTOM SIDEBAR PANEL
    ═══════════════════════════════════════════════════ */
    .rm-sidebar {
        position: fixed;
        top: 0; left: 0; bottom: 0;
        width: var(--sidebar-w);
        background: #0a0a0a;
        border-right: 1px solid #1e1e1e;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 1rem 0.75rem;
        z-index: 999;
        transform: translateX(0);
        transition: transform 0.25s ease;
        display: flex;
        flex-direction: column;
    }
    .rm-sidebar.closed {
        transform: translateX(calc(-1 * var(--sidebar-w)));
    }

    /* ═══════════════════════════════════════════════════
       MAIN CONTENT AREA
    ═══════════════════════════════════════════════════ */
    .rm-main {
        margin-left: var(--sidebar-w);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        transition: margin-left 0.25s ease;
    }
    .rm-main.full-width {
        margin-left: 0;
    }

    /* ═══════════════════════════════════════════════════
       TOP BAR
    ═══════════════════════════════════════════════════ */
    .rm-topbar {
        position: sticky;
        top: 0;
        z-index: 100;
        background: rgba(15,15,15,0.92);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
        height: var(--topbar-h);
        display: flex;
        align-items: center;
        padding: 0 1rem;
        gap: 0.5rem;
    }
    .rm-topbar-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #fff;
        letter-spacing: -0.02em;
        margin-right: auto;
    }
    .rm-topbar-btn {
        background: var(--surface2);
        border: 1px solid var(--border2);
        border-radius: 8px;
        color: var(--text2);
        cursor: pointer;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.35rem 0.75rem;
        transition: all 0.15s;
        white-space: nowrap;
        font-family: 'Inter', sans-serif;
    }
    .rm-topbar-btn:hover   { background: var(--surface3); color: var(--text); }
    .rm-topbar-btn.active  { background: var(--accent); border-color: var(--accent); color: #fff; }
    .rm-topbar-icon {
        background: transparent;
        border: 1px solid var(--border2);
        border-radius: 8px;
        color: var(--text2);
        cursor: pointer;
        font-size: 1rem;
        width: 34px; height: 34px;
        display: flex; align-items: center; justify-content: center;
        transition: all 0.15s;
        flex-shrink: 0;
    }
    .rm-topbar-icon:hover { background: var(--surface2); color: var(--text); }

    /* ═══════════════════════════════════════════════════
       MAIN CONTENT PADDING
    ═══════════════════════════════════════════════════ */
    .rm-content {
        padding: 1.25rem 1.5rem 3rem;
        flex: 1;
    }

    /* ═══════════════════════════════════════════════════
       SIDEBAR INTERNALS
    ═══════════════════════════════════════════════════ */
    .sidebar-brand {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #1e1e1e;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .sidebar-close-btn {
        background: transparent;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        color: #555;
        cursor: pointer;
        font-size: 0.9rem;
        width: 26px; height: 26px;
        display: none;           /* shown only on mobile via media query */
        align-items: center;
        justify-content: center;
        transition: all 0.15s;
    }
    .sidebar-close-btn:hover { color: #fff; border-color: #555; }

    /* ═══════════════════════════════════════════════════
       INPUTS
    ═══════════════════════════════════════════════════ */
    .stTextInput > div > div > input {
        background: var(--surface) !important;
        border: 1px solid var(--border2) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.9rem 1.2rem !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
        background: var(--surface2) !important;
    }
    .stTextInput > div > div > input::placeholder { color: var(--text3) !important; }

    /* ═══════════════════════════════════════════════════
       STREAMLIT BUTTONS
    ═══════════════════════════════════════════════════ */
    .stButton > button {
        background: var(--surface2) !important;
        color: var(--text) !important;
        border: 1px solid var(--border2) !important;
        border-radius: var(--radius) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        background: var(--surface3) !important;
        border-color: #444 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
        color: #fff !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--accent-hover) !important;
        border-color: var(--accent-hover) !important;
    }
    .stButton > button:disabled {
        opacity: 0.3 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    /* ═══════════════════════════════════════════════════
       STEP CARDS
    ═══════════════════════════════════════════════════ */
    .step-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.2rem 1.4rem; margin-bottom: 0.75rem; position: relative; overflow: hidden; transition: border-color 0.2s; }
    .step-card.active  { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent-soft); }
    .step-card.active::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg,#3b82f6,#2563eb); }
    .step-card.done    { border-color: rgba(16,185,129,0.3); }
    .step-card.error   { border-color: rgba(239,68,68,0.4); }
    .step-card.waiting { opacity: 0.4; }
    .step-header { display: flex; align-items: center; gap: 0.75rem; }
    .step-icon   { font-size: 1.1rem; width: 2rem; text-align: center; }
    .step-title  { font-weight: 600; font-size: 0.9rem; color: var(--text); }
    .step-meta   { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--text3); letter-spacing: 0.05em; margin-top: 1px; }
    .badge { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; padding: 2px 8px; border-radius: 99px; font-weight: 500; }
    .badge-active  { background: var(--accent-soft); color: #60a5fa; border: 1px solid rgba(37,99,235,0.2); }
    .badge-done    { background: var(--green-soft);  color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
    .badge-waiting { background: rgba(255,255,255,0.04); color: var(--text3); border: 1px solid var(--border); }
    .badge-error   { background: var(--danger-soft); color: #f87171; border: 1px solid rgba(239,68,68,0.2); }

    /* ═══════════════════════════════════════════════════
       TABS
    ═══════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: var(--radius) !important; padding: 4px !important; gap: 2px !important; border: 1px solid var(--border) !important; }
    .stTabs [data-baseweb="tab"] { font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 0.82rem !important; color: var(--text2) !important; border-radius: 8px !important; padding: 0.4rem 1rem !important; }
    .stTabs [aria-selected="true"] { background: var(--surface2) !important; color: var(--text) !important; }

    /* ═══════════════════════════════════════════════════
       CONTENT BOXES
    ═══════════════════════════════════════════════════ */
    .content-box { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.4rem 1.6rem; font-size: 0.88rem; line-height: 1.8; color: var(--text2); white-space: pre-wrap; word-break: break-word; max-height: 480px; overflow-y: auto; }
    .report-box  { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.8rem 2rem; line-height: 1.85; font-size: 0.92rem; color: var(--text); white-space: pre-wrap; word-break: break-word; }

    /* ═══════════════════════════════════════════════════
       METRICS
    ═══════════════════════════════════════════════════ */
    .metric-row  { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
    .metric-chip { flex: 1; min-width: 80px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.9rem 1rem; text-align: center; }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #60a5fa; letter-spacing: -0.03em; line-height: 1; }
    .metric-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 4px; }

    /* ═══════════════════════════════════════════════════
       SECTION
    ═══════════════════════════════════════════════════ */
    .section-title { font-weight: 600; font-size: 1rem; color: var(--text); letter-spacing: -0.02em; margin-bottom: 0.2rem; }
    .section-sub   { font-size: 0.8rem; color: var(--text3); margin-bottom: 1rem; }

    /* ═══════════════════════════════════════════════════
       CHAT
    ═══════════════════════════════════════════════════ */
    .chat-container { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1rem; margin-top: 0.75rem; max-height: 400px; overflow-y: auto; }
    .chat-msg       { margin-bottom: 0.75rem; }
    .chat-msg-user  { background: var(--accent-soft); border: 1px solid rgba(37,99,235,0.2); border-radius: 14px 14px 4px 14px; padding: 0.65rem 1rem; font-size: 0.88rem; color: var(--text); margin-left: 1.5rem; line-height: 1.6; }
    .chat-msg-ai    { background: var(--surface2); border: 1px solid var(--border); border-radius: 14px 14px 14px 4px; padding: 0.65rem 1rem; font-size: 0.88rem; color: var(--text2); margin-right: 1.5rem; line-height: 1.7; white-space: pre-wrap; }
    .chat-label     { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--text3); letter-spacing: 0.08em; margin-bottom: 3px; text-transform: uppercase; }

    /* ═══════════════════════════════════════════════════
       HERO
    ═══════════════════════════════════════════════════ */
    .hero { padding: 2rem 0 1.5rem; max-width: 700px; }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: var(--accent-soft); border: 1px solid rgba(37,99,235,0.25);
        border-radius: 99px; padding: 4px 12px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
        color: #60a5fa; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 1rem;
    }
    .hero h1 { font-size: clamp(1.5rem, 4vw, 3rem); font-weight: 700; line-height: 1.1; letter-spacing: -0.03em; color: #ffffff; margin: 0 0 0.6rem; }
    .hero h1 span { background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .hero-sub { color: var(--text2); font-size: 0.92rem; line-height: 1.7; max-width: 540px; margin: 0; }

    /* ═══════════════════════════════════════════════════
       GUEST BANNER
    ═══════════════════════════════════════════════════ */
    .guest-banner { background: linear-gradient(135deg,#1a1a2e,#16213e); border: 1px solid rgba(37,99,235,0.3); border-radius: var(--radius); padding: 0.6rem 0.9rem; margin-bottom: 0.75rem; font-size: 0.78rem; color: #93c5fd; }

    /* ═══════════════════════════════════════════════════
       PDF BAR
    ═══════════════════════════════════════════════════ */
    .pdf-bar       { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.8rem 1.2rem; display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem; flex-wrap: wrap; }
    .pdf-bar-name  { font-weight: 600; font-size: 0.9rem; color: var(--text); }
    .pdf-bar-meta  { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--text3); }
    .pdf-bar-badge { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #34d399; background: var(--green-soft); padding: 2px 8px; border-radius: 99px; border: 1px solid rgba(16,185,129,0.2); }

    /* ═══════════════════════════════════════════════════
       AUTH
    ═══════════════════════════════════════════════════ */
    .auth-logo       { text-align: center; margin-bottom: 2rem; }
    .auth-logo-icon  { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .auth-logo-title { font-size: 1.5rem; font-weight: 700; color: #fff; letter-spacing: -0.03em; }
    .auth-logo-sub   { font-size: 0.82rem; color: var(--text3); margin-top: 4px; }
    .auth-divider    { display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0; color: var(--text3); font-size: 0.75rem; }
    .auth-divider::before, .auth-divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }

    /* ═══════════════════════════════════════════════════
       MISC
    ═══════════════════════════════════════════════════ */
    hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
    .stProgress > div > div { background: var(--accent) !important; border-radius: 99px !important; }
    .stAlert { border-radius: var(--radius) !important; font-size: 0.88rem !important; }
    .streamlit-expanderHeader { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; font-weight: 500 !important; font-size: 0.85rem !important; color: var(--text2) !important; }

    /* ═══════════════════════════════════════════════════
       TABLET  (≤ 1024px) — sidebar collapses to drawer
    ═══════════════════════════════════════════════════ */
    @media (max-width: 1024px) {
        .rm-sidebar {
            transform: translateX(calc(-1 * var(--sidebar-w)));
            box-shadow: 4px 0 24px rgba(0,0,0,0.6);
        }
        .rm-sidebar.open {
            transform: translateX(0);
        }
        .rm-main {
            margin-left: 0 !important;
        }
        .sidebar-close-btn {
            display: flex !important;
        }
        .rm-content {
            padding: 1rem 1rem 4rem;
        }
    }

    /* ═══════════════════════════════════════════════════
       MOBILE  (≤ 640px)
    ═══════════════════════════════════════════════════ */
    @media (max-width: 640px) {
        :root { --sidebar-w: 280px; }

        .rm-topbar { padding: 0 0.75rem; gap: 0.35rem; }
        .rm-topbar-btn { font-size: 0.78rem; padding: 0.3rem 0.6rem; }
        .rm-topbar-title { font-size: 0.88rem; }

        .rm-content { padding: 0.75rem 0.75rem 5rem; }

        /* Stack step cards on mobile */
        .step-card { padding: 0.9rem 1rem; }
        .step-title { font-size: 0.82rem; }
        .step-meta  { font-size: 0.6rem; }

        /* Full-width content boxes */
        .content-box, .report-box { padding: 1rem 1.1rem; font-size: 0.85rem; }

        /* Chat bubbles — tighter margins on mobile */
        .chat-msg-user { margin-left: 0.5rem; }
        .chat-msg-ai   { margin-right: 0.5rem; }

        /* Hero */
        .hero { padding: 1rem 0 1rem; }
        .hero h1 { font-size: clamp(1.4rem, 7vw, 2rem); }
        .hero-sub { font-size: 0.85rem; }

        /* Metric chips wrap nicely */
        .metric-chip { min-width: 70px; padding: 0.7rem 0.6rem; }
        .metric-value { font-size: 1.2rem; }

        /* Tabs scroll horizontally */
        .stTabs [data-baseweb="tab-list"] { overflow-x: auto !important; flex-wrap: nowrap !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.75rem !important; padding: 0.35rem 0.7rem !important; white-space: nowrap !important; }

        /* Streamlit columns inside sidebar full-width */
        .rm-sidebar .stHorizontalBlock { flex-direction: column; gap: 0.4rem; }
    }
    </style>
    """, unsafe_allow_html=True)