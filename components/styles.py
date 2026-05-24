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
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg);
        color: var(--text);
        -webkit-font-smoothing: antialiased;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1rem 2rem 3rem !important; max-width: 100%; }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 99px; }

    /* ── Native sidebar styling ── */
    [data-testid="stSidebar"] {
        background: #0a0a0a !important;
        border-right: 1px solid #1e1e1e !important;
    }

    /* FIX: target the actual scrollable content container instead of > div */
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
        padding: 1rem 0.75rem !important;
        overflow-y: auto !important;
    }

    /* FIX: collapse the native sidebar header so it doesn't eat space */
    [data-testid="stSidebarHeader"] {
        padding: 0 !important;
        min-height: 0 !important;
    }

    /* ── Style the native collapse button ── */
    [data-testid="collapsedControl"] {
        background: #0a0a0a !important;
        border-right: 1px solid #1e1e1e !important;
        width: 2rem !important;
    }
    [data-testid="collapsedControl"] button {
        color: #555 !important;
        background: transparent !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        width: 28px !important;
        height: 28px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0.5rem auto !important;
    }
    [data-testid="collapsedControl"] button:hover {
        color: #fff !important;
        border-color: #444 !important;
        background: #1e1e1e !important;
    }

    /* ── Also style the in-sidebar collapse button ── */
    button[data-testid="baseButton-header"] {
        color: #555 !important;
        background: transparent !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
    }
    button[data-testid="baseButton-header"]:hover {
        color: #fff !important;
        border-color: #555 !important;
        background: #1e1e1e !important;
    }

    /* ── Hero ── */
    .hero { padding: 2rem 0 1.5rem; max-width: 700px; }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--accent-soft);
        border: 1px solid rgba(37,99,235,0.25);
        border-radius: 99px;
        padding: 4px 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #60a5fa;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero h1 {
        font-size: clamp(1.8rem, 3.5vw, 3rem);
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 0 0 0.6rem;
    }
    .hero h1 span {
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub { color: var(--text2); font-size: 0.95rem; line-height: 1.7; max-width: 540px; margin: 0; }

    /* ── Inputs ── */
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

    /* ── Buttons ── */
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
    .stButton > button:disabled { opacity: 0.3 !important; cursor: not-allowed !important; transform: none !important; }

    /* ── Step cards ── */
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

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: var(--radius) !important; padding: 4px !important; gap: 2px !important; border: 1px solid var(--border) !important; }
    .stTabs [data-baseweb="tab"] { font-family: 'Inter', sans-serif !important; font-weight: 500 !important; font-size: 0.82rem !important; color: var(--text2) !important; border-radius: 8px !important; padding: 0.4rem 1rem !important; }
    .stTabs [aria-selected="true"] { background: var(--surface2) !important; color: var(--text) !important; }

    /* ── Content boxes ── */
    .content-box { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.4rem 1.6rem; font-size: 0.88rem; line-height: 1.8; color: var(--text2); white-space: pre-wrap; word-break: break-word; max-height: 480px; overflow-y: auto; }
    .report-box  { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.8rem 2rem; line-height: 1.85; font-size: 0.92rem; color: var(--text); white-space: pre-wrap; word-break: break-word; }

    /* ── Metrics ── */
    .metric-row  { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; }
    .metric-chip { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.9rem 1rem; text-align: center; }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #60a5fa; letter-spacing: -0.03em; line-height: 1; }
    .metric-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 4px; }

    /* ── Section ── */
    .section-title { font-weight: 600; font-size: 1rem; color: var(--text); letter-spacing: -0.02em; margin-bottom: 0.2rem; }
    .section-sub   { font-size: 0.8rem; color: var(--text3); margin-bottom: 1rem; }

    /* ── Chat ── */
    .chat-container { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1rem; margin-top: 0.75rem; max-height: 400px; overflow-y: auto; }
    .chat-msg       { margin-bottom: 0.75rem; }
    .chat-msg-user  { background: var(--accent-soft); border: 1px solid rgba(37,99,235,0.2); border-radius: 14px 14px 4px 14px; padding: 0.65rem 1rem; font-size: 0.88rem; color: var(--text); margin-left: 2.5rem; line-height: 1.6; }
    .chat-msg-ai    { background: var(--surface2); border: 1px solid var(--border); border-radius: 14px 14px 14px 4px; padding: 0.65rem 1rem; font-size: 0.88rem; color: var(--text2); margin-right: 2.5rem; line-height: 1.7; white-space: pre-wrap; }
    .chat-label     { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--text3); letter-spacing: 0.08em; margin-bottom: 3px; text-transform: uppercase; }

    /* ── Sidebar brand ── */
    .sidebar-brand { font-size: 1rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; padding-bottom: 0.75rem; border-bottom: 1px solid #1e1e1e; margin-bottom: 1rem; }

    /* ── Guest banner ── */
    .guest-banner { background: linear-gradient(135deg,#1a1a2e,#16213e); border: 1px solid rgba(37,99,235,0.3); border-radius: var(--radius); padding: 0.6rem 0.9rem; margin-bottom: 0.75rem; font-size: 0.78rem; color: #93c5fd; }

    /* ── PDF bar ── */
    .pdf-bar       { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.8rem 1.2rem; display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem; }
    .pdf-bar-name  { font-weight: 600; font-size: 0.9rem; color: var(--text); }
    .pdf-bar-meta  { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--text3); }
    .pdf-bar-badge { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #34d399; background: var(--green-soft); padding: 2px 8px; border-radius: 99px; border: 1px solid rgba(16,185,129,0.2); }

    /* ── Auth ── */
    .auth-logo       { text-align: center; margin-bottom: 2rem; }
    .auth-logo-icon  { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .auth-logo-title { font-size: 1.5rem; font-weight: 700; color: #fff; letter-spacing: -0.03em; }
    .auth-logo-sub   { font-size: 0.82rem; color: var(--text3); margin-top: 4px; }
    .auth-divider    { display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0; color: var(--text3); font-size: 0.75rem; }
    .auth-divider::before, .auth-divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }

    /* ── Misc ── */
    hr { border-color: var(--border) !important; margin: 1.25rem 0 !important; }
    .stProgress > div > div { background: var(--accent) !important; border-radius: 99px !important; }
    .stAlert { border-radius: var(--radius) !important; font-size: 0.88rem !important; }
    .streamlit-expanderHeader { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; font-weight: 500 !important; font-size: 0.85rem !important; color: var(--text2) !important; }
    </style>
    """, unsafe_allow_html=True)