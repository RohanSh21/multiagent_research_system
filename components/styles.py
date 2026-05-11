import streamlit as st


def load_styles() -> None:
    """Injects all custom CSS into the Streamlit app."""

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

    :root {
        --bg:        #0a0b0f;
        --surface:   #111318;
        --surface2:  #181c24;
        --border:    #232838;
        --accent:    #4fffb0;
        --accent2:   #38bdf8;
        --accent3:   #f472b6;
        --text:      #e8eaf0;
        --muted:     #6b7280;
        --danger:    #f87171;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--bg);
        color: var(--text);
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

    /* ── HERO ── */
    .hero {
        text-align: center;
        padding: 3.5rem 1rem 2.5rem;
    }
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
        font-size: clamp(2.4rem, 5vw, 4rem);
        font-weight: 800;
        line-height: 1.05;
        background: linear-gradient(135deg, #fff 30%, var(--accent) 70%, var(--accent2) 100%);
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
        margin: 0 auto 2rem;
        line-height: 1.65;
    }

    /* ── TEXT INPUT ── */
    .stTextInput > div > div > input {
        background: var(--surface) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.85rem 1.2rem !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(79,255,176,0.12) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: var(--muted) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
        color: #0a0b0f !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.04em !important;
        padding: 0.7rem 2rem !important;
        transition: opacity 0.2s, transform 0.15s !important;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active  { transform: translateY(0) !important; }
    .stButton > button:disabled { opacity: 0.35 !important; cursor: not-allowed !important; }

    /* ── PIPELINE STEP CARDS ── */
    .step-card {
        background: var(--surface);
        border: 1.5px solid var(--border);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }
    .step-card.active  { border-color: var(--accent); }
    .step-card.done    { border-color: #2e4a3b; }
    .step-card.error   { border-color: var(--danger); }
    .step-card.waiting { opacity: 0.45; }
    .step-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
        opacity: 0;
        transition: opacity 0.3s;
    }
    .step-card.active::before { opacity: 1; }
    .step-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.3rem;
    }
    .step-icon  { font-size: 1.3rem; width: 2.2rem; text-align: center; }
    .step-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; color: var(--text); }
    .step-meta  { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: var(--muted); letter-spacing: 0.08em; }

    /* ── BADGES ── */
    .badge {
        margin-left: auto;
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-weight: 500;
    }
    .badge-active  { background: rgba(79,255,176,0.15);  color: var(--accent); }
    .badge-done    { background: rgba(79,255,176,0.08);  color: #4fffb0aa; }
    .badge-waiting { background: rgba(107,114,128,0.12); color: var(--muted); }
    .badge-error   { background: rgba(248,113,113,0.15); color: var(--danger); }

    /* ── RESULT TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: 1.5px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        color: var(--muted) !important;
        border-radius: 7px !important;
        padding: 0.45rem 1.1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--surface2) !important;
        color: var(--text) !important;
    }

    /* ── CONTENT BOXES ── */
    .content-box {
        background: var(--surface);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        font-size: 0.93rem;
        line-height: 1.75;
        color: var(--text);
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 500px;
        overflow-y: auto;
    }
    .content-box::-webkit-scrollbar       { width: 5px; }
    .content-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

    .report-box {
        background: var(--surface);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 2rem 2.4rem;
        line-height: 1.85;
        font-size: 0.95rem;
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* ── METRICS ── */
    .metric-row  { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    .metric-chip {
        flex: 1;
        background: var(--surface);
        border: 1.5px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--accent);
    }
    .metric-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        color: var(--muted);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.15rem;
    }

    /* ── SECTION TITLES ── */
    .section-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--text);
        margin-bottom: 0.2rem;
    }
    .section-sub {
        font-size: 0.82rem;
        color: var(--muted);
        margin-bottom: 1rem;
    }

    /* ── CHAT ── */
    .chat-container {
        background: var(--surface);
        border: 1.5px solid var(--border);
        border-radius: 14px;
        padding: 1.2rem;
        margin-top: 0.8rem;
        max-height: 420px;
        overflow-y: auto;
    }
    .chat-container::-webkit-scrollbar       { width: 5px; }
    .chat-container::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

    .chat-msg { margin-bottom: 1rem; }
    .chat-msg-user {
        background: rgba(79,255,176,0.07);
        border: 1px solid rgba(79,255,176,0.15);
        border-radius: 12px 12px 4px 12px;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        color: var(--text);
        margin-left: 3rem;
    }
    .chat-msg-ai {
        background: var(--surface2);
        border: 1px solid var(--border);
        border-radius: 12px 12px 12px 4px;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        color: var(--text);
        margin-right: 3rem;
        line-height: 1.65;
        white-space: pre-wrap;
    }
    .chat-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        color: var(--muted);
        letter-spacing: 0.08em;
        margin-bottom: 0.25rem;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1.5px solid var(--border) !important;
    }
    .sidebar-brand {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.1rem;
        color: var(--accent);
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.2rem;
    }
    .history-item {
        background: var(--surface2);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.82rem;
        color: var(--muted);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* ── PDF INFO BAR ── */
    .pdf-bar {
        background: var(--surface);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        padding: 0.9rem 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1.2rem;
    }
    .pdf-bar-name {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        color: var(--text);
    }
    .pdf-bar-meta {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: var(--muted);
    }
    .pdf-bar-badge {
        margin-left: auto;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent);
        background: rgba(79,255,176,0.1);
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
    }

    /* ── MISC ── */
    hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
    .stProgress > div > div  { background: var(--accent) !important; }
    .stAlert { border-radius: 10px !important; }
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        color: var(--text) !important;
    }
    </style>
    """, unsafe_allow_html=True)