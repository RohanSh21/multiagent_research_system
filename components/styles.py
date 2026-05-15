import streamlit as st


def load_styles() -> None:
    """Injects all custom CSS — modern dark UI."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

    :root {
        --bg:        #090909;
        --surface:   #111111;
        --surface2:  #1a1a1a;
        --border:    #2b2b2b;
        --accent:    #3b82f6;
        --accent2:   #2563eb;
        --accent3:   #1d4ed8;
        --text:      #f5f5f5;
        --muted:     #9ca3af;
        --danger:    #ef4444;
        --shadow:    rgba(0,0,0,0.45);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem 2rem; max-width: 100%; }

    /* ── Hero ── */
    .hero { text-align: left; padding: 1rem 0 2rem; }
    .hero-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.25em;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero h1 {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.2rem, 4vw, 3.4rem);
        font-weight: 800;
        line-height: 1.05;
        background: linear-gradient(90deg,#ffffff 0%,#d4d4d4 55%,#3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.75rem;
    }
    .hero-sub {
        color: var(--muted);
        font-size: 1.05rem;
        font-weight: 300;
        max-width: 560px;
        margin: 0 0 2rem;
        line-height: 1.65;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input {
        background: #141414 !important;
        border: 1px solid #303030 !important;
        border-radius: 16px !important;
        color: #f5f5f5 !important;
        font-size: 0.95rem !important;
        padding: 1rem 1.2rem !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }
    .stTextInput > div > div > input::placeholder { color: #9ca3af !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg,#1f1f1f,#2a2a2a) !important;
        color: #ffffff !important;
        border: 1px solid #323232 !important;
        border-radius: 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        padding: 0.9rem 1.2rem !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.28) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg,#2d2d2d,#3a3a3a) !important;
        border: 1px solid #3b82f6 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(0,0,0,0.32) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }
    .stButton > button:disabled { opacity: 0.35 !important; cursor: not-allowed !important; }

    /* ── Cards ── */
    .step-card,
    .content-box,
    .report-box,
    .metric-chip,
    .chat-container {
        background: rgba(18,18,18,0.82) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.05) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.18);
    }

    .step-card {
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }
    .step-card.active  { border-color: #3b82f6 !important; }
    .step-card.done    { border-color: #1e3a2f !important; }
    .step-card.error   { border-color: var(--danger) !important; }
    .step-card.waiting { opacity: 0.45; }
    .step-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .step-card.active::before { opacity: 1; }

    .step-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.3rem; }
    .step-icon { font-size: 1.3rem; width: 2.2rem; text-align: center; }
    .step-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; color: #f5f5f5; }
    .step-meta { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #9ca3af; letter-spacing: 0.08em; }

    /* ── Badges ── */
    .badge { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; padding: 0.2rem 0.6rem; border-radius: 999px; font-weight: 500; }
    .badge-active  { background: rgba(59,130,246,0.15); color: #60a5fa; }
    .badge-done    { background: rgba(59,130,246,0.08); color: #60a5faaa; }
    .badge-waiting { background: rgba(107,114,128,0.12); color: #9ca3af; }
    .badge-error   { background: rgba(239,68,68,0.15); color: #ef4444; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #111111 !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: 1px solid #2b2b2b !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        color: #9ca3af !important;
        border-radius: 7px !important;
        padding: 0.45rem 1.1rem !important;
    }
    .stTabs [aria-selected="true"] { background: #1f1f1f !important; color: #ffffff !important; }

    /* ── Content boxes ── */
    .content-box {
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        font-size: 0.93rem;
        line-height: 1.75;
        color: #f5f5f5;
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 500px;
        overflow-y: auto;
    }
    .content-box::-webkit-scrollbar { width: 5px; }
    .content-box::-webkit-scrollbar-thumb { background: #2b2b2b; border-radius: 4px; }

    .report-box {
        border-radius: 12px;
        padding: 2rem 2.4rem;
        line-height: 1.85;
        font-size: 0.95rem;
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* ── Metrics ── */
    .metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    .metric-chip { flex: 1; border-radius: 10px; padding: 1rem 1.2rem; text-align: center; }
    .metric-value { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; color: #3b82f6; }
    .metric-label { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: #9ca3af; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.15rem; }

    /* ── Section titles ── */
    .section-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.1rem; color: #f5f5f5; margin-bottom: 0.2rem; }
    .section-sub { font-size: 0.82rem; color: #9ca3af; margin-bottom: 1rem; }

    /* ── Chat ── */
    .chat-container { border-radius: 14px; padding: 1.2rem; margin-top: 0.8rem; max-height: 420px; overflow-y: auto; }
    .chat-container::-webkit-scrollbar { width: 5px; }
    .chat-container::-webkit-scrollbar-thumb { background: #2b2b2b; border-radius: 4px; }
    .chat-msg { margin-bottom: 1rem; }
    .chat-msg-user {
        background: rgba(59,130,246,0.12);
        border: 1px solid rgba(59,130,246,0.22);
        border-radius: 12px 12px 4px 12px;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        color: #f5f5f5;
        margin-left: 3rem;
    }
    .chat-msg-ai {
        background: #1a1a1a;
        border: 1px solid #2c2c2c;
        border-radius: 12px 12px 12px 4px;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        color: #f5f5f5;
        margin-right: 3rem;
        line-height: 1.65;
        white-space: pre-wrap;
    }
    .chat-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #9ca3af; letter-spacing: 0.08em; margin-bottom: 0.25rem; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0d0d0d !important;
        border-right: 1px solid #262626 !important;
        min-width: 290px !important;
        max-width: 290px !important;
        padding-top: 1rem !important;
        box-shadow: none !important;
        transform: translateX(0%) !important;
        visibility: visible !important;
        z-index: 999999 !important;
    }
    .sidebar-brand {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.1rem;
        color: #ffffff;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #2b2b2b;
        margin-bottom: 1.2rem;
    }
    .history-item {
        background: #1a1a1a;
        border: 1px solid #2b2b2b;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.82rem;
        color: #9ca3af;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* ── PDF bar ── */
    .pdf-bar {
        background: #111111;
        border: 1px solid #2b2b2b;
        border-radius: 12px;
        padding: 0.9rem 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1.2rem;
    }
    .pdf-bar-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: #f5f5f5; }
    .pdf-bar-meta { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #9ca3af; }
    .pdf-bar-badge { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #60a5fa; background: rgba(59,130,246,0.12); padding: 0.2rem 0.7rem; border-radius: 999px; }

    /* ── Misc ── */
    hr { border-color: #2b2b2b !important; margin: 1.5rem 0 !important; }
    .stProgress > div > div { background: #3b82f6 !important; }
    .stAlert { border-radius: 10px !important; }
    .streamlit-expanderHeader {
        background: #111111 !important;
        border: 1px solid #2b2b2b !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)