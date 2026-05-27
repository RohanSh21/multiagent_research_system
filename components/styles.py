import streamlit as st


def load_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ═══════════════════════════════════════════════════
       DESIGN TOKENS
    ═══════════════════════════════════════════════════ */
    :root {
        --bg:           #0d0d0d;
        --surface:      #141414;
        --surface2:     #1a1a1a;
        --surface3:     #202020;
        --surface4:     #272727;
        --border:       #262626;
        --border2:      #303030;
        --border3:      #3a3a3a;
        --accent:       #2f6feb;
        --accent-hover: #2563d4;
        --accent-dim:   rgba(47,111,235,0.15);
        --accent-glow:  rgba(47,111,235,0.08);
        --green:        #22c55e;
        --green-dim:    rgba(34,197,94,0.12);
        --amber:        #f59e0b;
        --amber-dim:    rgba(245,158,11,0.12);
        --red:          #ef4444;
        --red-dim:      rgba(239,68,68,0.12);
        --text:         #f0f0f0;
        --text2:        #9a9a9a;
        --text3:        #5a5a5a;
        --text4:        #3a3a3a;
        --r-sm:   8px;
        --r-md:   12px;
        --r-lg:   16px;
        --r-xl:   20px;
        --r-full: 999px;
    }

    /* ═══════════════════════════════════════════════════
       BASE
    ═══════════════════════════════════════════════════ */
    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg) !important;
        color: var(--text);
        -webkit-font-smoothing: antialiased;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding: 1rem 1.5rem 3rem !important; max-width: 100% !important; }

    ::-webkit-scrollbar       { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #303030; border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: #404040; }

    /* ═══════════════════════════════════════════════════
       SIDEBAR PANEL (inside left column)
    ═══════════════════════════════════════════════════ */
    .sidebar-brand {
        font-size: 0.95rem; font-weight: 600; color: var(--text);
        letter-spacing: -0.01em;
        padding: 0.25rem 0.25rem 0.875rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 0.875rem;
        display: flex; align-items: center; justify-content: space-between;
    }
    .sidebar-brand-logo { display: flex; align-items: center; gap: 0.5rem; }

    .sidebar-section-label {
        font-size: 0.65rem; font-weight: 600; color: var(--text3);
        letter-spacing: 0.08em; text-transform: uppercase;
        padding: 0 0.25rem; margin-bottom: 0.35rem; margin-top: 0.25rem;
    }

    .sidebar-user-row {
        display: flex; align-items: center; gap: 0.5rem;
        padding: 0.5rem; border-radius: var(--r-md);
        background: var(--surface); border: 1px solid var(--border);
        margin-bottom: 0.75rem;
    }
    .sidebar-avatar {
        width: 28px; height: 28px; border-radius: 50%;
        background: var(--accent-dim); border: 1px solid rgba(47,111,235,0.3);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; color: #93c5fd; font-weight: 600; flex-shrink: 0;
    }
    .sidebar-username {
        font-size: 0.78rem; font-weight: 500; color: var(--text2);
        flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }

    .sidebar-section-label {
        font-size: 0.65rem; font-weight: 600; color: var(--text3);
        letter-spacing: 0.08em; text-transform: uppercase;
        padding: 0 0.25rem; margin-bottom: 0.35rem; margin-top: 0.1rem;
    }

    .agent-chip {
        display: flex; align-items: center; gap: 0.6rem;
        padding: 0.4rem 0.5rem; border-radius: var(--r-sm); margin-bottom: 0.1rem;
    }
    .agent-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); flex-shrink: 0; }
    .agent-name { font-size: 0.78rem; font-weight: 500; color: var(--text2); }
    .agent-desc { font-size: 0.64rem; color: var(--text3); font-family: 'JetBrains Mono', monospace; }

    .thread-group-label {
        font-size: 0.62rem; font-weight: 500; color: var(--text3);
        letter-spacing: 0.06em; text-transform: uppercase;
        padding: 0.5rem 0.25rem 0.2rem; font-family: 'JetBrains Mono', monospace;
    }

    .sidebar-footer {
        margin-top: 1rem; padding-top: 0.875rem;
        border-top: 1px solid var(--border);
        font-size: 0.62rem; color: var(--text4);
        font-family: 'JetBrains Mono', monospace; padding-left: 0.25rem;
    }

    /* ═══════════════════════════════════════════════════
       GUEST BANNER
    ═══════════════════════════════════════════════════ */
    .guest-banner {
        display: flex; align-items: center; gap: 0.5rem;
        background: linear-gradient(135deg, rgba(47,111,235,0.1), rgba(37,99,212,0.05));
        border: 1px solid rgba(47,111,235,0.2);
        border-radius: var(--r-md); padding: 0.6rem 0.875rem;
        margin-bottom: 0.75rem; font-size: 0.78rem; color: #93c5fd; line-height: 1.4;
    }

    /* ═══════════════════════════════════════════════════
       MODEL BADGE
    ═══════════════════════════════════════════════════ */
    .model-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: var(--surface2); border: 1px solid var(--border2);
        border-radius: var(--r-full); padding: 4px 10px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--green);
        margin-bottom: 1rem;
    }
    .model-badge-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--green); flex-shrink: 0; }

    /* ═══════════════════════════════════════════════════
       STREAMLIT WIDGET OVERRIDES
    ═══════════════════════════════════════════════════ */
    .stTextInput > div > div > input {
        background: var(--surface) !important;
        border: 1px solid var(--border2) !important;
        border-radius: var(--r-lg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.875rem 1.2rem !important;
        transition: all 0.15s !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
        background: var(--surface2) !important;
    }
    .stTextInput > div > div > input::placeholder { color: var(--text3) !important; }
    .stTextInput label { display: none !important; }

    .stButton > button {
        background: var(--surface2) !important;
        color: var(--text2) !important;
        border: 1px solid var(--border2) !important;
        border-radius: var(--r-md) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important; font-size: 0.85rem !important;
        padding: 0.55rem 1rem !important;
        transition: all 0.15s !important; box-shadow: none !important;
        letter-spacing: -0.01em !important;
    }
    .stButton > button:hover {
        background: var(--surface3) !important;
        border-color: var(--border3) !important; color: var(--text) !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important; color: #fff !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--accent-hover) !important;
        border-color: var(--accent-hover) !important;
        box-shadow: 0 4px 12px rgba(47,111,235,0.25) !important;
    }
    .stButton > button:disabled { opacity: 0.3 !important; cursor: not-allowed !important; }

    .stSelectbox > div > div {
        background: var(--surface) !important;
        border: 1px solid var(--border2) !important;
        border-radius: var(--r-md) !important; color: var(--text) !important;
    }
    .stSelectbox label { color: var(--text3) !important; font-size: 0.75rem !important; }

    [data-testid="stFileUploader"] {
        background: var(--surface) !important;
        border: 2px dashed var(--border2) !important;
        border-radius: var(--r-lg) !important; transition: border-color 0.15s !important;
    }
    [data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }

    .stProgress > div > div { background: var(--accent) !important; border-radius: 99px !important; }
    .stProgress > div { background: var(--surface2) !important; border-radius: 99px !important; }

    .stAlert { border-radius: var(--r-md) !important; font-size: 0.85rem !important; border: 1px solid var(--border2) !important; }

    .streamlit-expanderHeader {
        background: var(--surface) !important; border: 1px solid var(--border) !important;
        border-radius: var(--r-md) !important; font-weight: 500 !important;
        font-size: 0.83rem !important; color: var(--text2) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface) !important; border-radius: var(--r-md) !important;
        padding: 3px !important; gap: 2px !important; border: 1px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important; font-weight: 500 !important;
        font-size: 0.82rem !important; color: var(--text3) !important;
        border-radius: var(--r-sm) !important; padding: 0.38rem 0.9rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--surface2) !important; color: var(--text) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
    }

    .stRadio > div { gap: 0.5rem !important; }
    .stRadio label { color: var(--text2) !important; font-size: 0.85rem !important; }

    hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

    /* ═══════════════════════════════════════════════════
       HERO
    ═══════════════════════════════════════════════════ */
    .hero { padding: 2rem 0 1.5rem; max-width: 680px; }
    .hero-eyebrow {
        display: inline-flex; align-items: center; gap: 6px;
        background: var(--accent-dim); border: 1px solid rgba(47,111,235,0.2);
        border-radius: var(--r-full); padding: 4px 12px;
        font-size: 0.68rem; font-weight: 500; color: #93c5fd;
        letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1.1rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .hero h1 {
        font-size: clamp(1.75rem, 4vw, 2.75rem); font-weight: 700;
        line-height: 1.1; letter-spacing: -0.04em; color: #fff; margin: 0 0 0.75rem;
    }
    .hero h1 em {
        font-style: normal;
        background: linear-gradient(135deg, #93c5fd 0%, #60a5fa 50%, #2f6feb 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .hero-sub { color: var(--text2); font-size: 0.92rem; line-height: 1.75; max-width: 520px; margin: 0; }

    /* ═══════════════════════════════════════════════════
       PIPELINE STEPS
    ═══════════════════════════════════════════════════ */
    .step-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--r-lg); padding: 1.1rem 1.2rem;
        position: relative; overflow: hidden; transition: border-color 0.2s, box-shadow 0.2s;
        margin-bottom: 0.5rem;
    }
    .step-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: transparent; transition: background 0.2s;
    }
    .step-card.active  { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent-dim); }
    .step-card.active::before { background: linear-gradient(90deg, #60a5fa, var(--accent)); }
    .step-card.done    { border-color: rgba(34,197,94,0.35); }
    .step-card.done::before { background: linear-gradient(90deg, #4ade80, #22c55e); }
    .step-card.error   { border-color: rgba(239,68,68,0.35); }
    .step-card.waiting { opacity: 0.45; }
    .step-header { display: flex; align-items: flex-start; gap: 0.65rem; margin-bottom: 0.5rem; }
    .step-icon-wrap {
        width: 32px; height: 32px; border-radius: var(--r-sm);
        background: var(--surface2); border: 1px solid var(--border2);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.95rem; flex-shrink: 0;
    }
    .step-title  { font-weight: 600; font-size: 0.85rem; color: var(--text); line-height: 1.3; }
    .step-label  { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--text3); letter-spacing: 0.06em; margin-top: 1px; }
    .step-desc   { font-size: 0.75rem; color: var(--text3); line-height: 1.5; }
    .step-badge  {
        margin-left: auto; font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem; padding: 2px 7px; border-radius: var(--r-full);
        font-weight: 500; white-space: nowrap; flex-shrink: 0;
    }
    .badge-active  { background: var(--accent-dim); color: #93c5fd; border: 1px solid rgba(47,111,235,0.25); }
    .badge-done    { background: var(--green-dim);  color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
    .badge-waiting { background: rgba(255,255,255,0.03); color: var(--text3); border: 1px solid var(--border); }
    .badge-error   { background: var(--red-dim);   color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

    /* ═══════════════════════════════════════════════════
       METRICS
    ═══════════════════════════════════════════════════ */
    .metric-row { display: flex; gap: 0.75rem; margin: 1.25rem 0; flex-wrap: wrap; }
    .metric-chip {
        flex: 1; min-width: 80px; background: var(--surface);
        border: 1px solid var(--border); border-radius: var(--r-lg);
        padding: 1rem 1.1rem; text-align: center;
    }
    .metric-value { font-size: 1.4rem; font-weight: 700; color: #93c5fd; letter-spacing: -0.03em; line-height: 1; }
    .metric-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; margin-top: 5px; }

    /* ═══════════════════════════════════════════════════
       CONTENT / REPORT BOXES
    ═══════════════════════════════════════════════════ */
    .content-box {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--r-lg); padding: 1.25rem 1.5rem;
        font-size: 0.875rem; line-height: 1.8; color: var(--text2);
        white-space: pre-wrap; word-break: break-word;
        max-height: 500px; overflow-y: auto;
    }
    .report-box {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--r-lg); padding: 1.75rem 2rem;
        line-height: 1.9; font-size: 0.9rem; color: var(--text);
        white-space: pre-wrap; word-break: break-word;
    }

    /* ═══════════════════════════════════════════════════
       SECTION HEADERS
    ═══════════════════════════════════════════════════ */
    .section-header { margin: 1.5rem 0 0.75rem; }
    .section-title  { font-weight: 600; font-size: 0.95rem; color: var(--text); letter-spacing: -0.02em; }
    .section-sub    { font-size: 0.78rem; color: var(--text3); margin-top: 0.2rem; }

    /* ═══════════════════════════════════════════════════
       CHAT
    ═══════════════════════════════════════════════════ */
    .chat-wrap {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--r-lg); overflow: hidden; margin-top: 0.75rem;
    }
    .chat-messages {
        padding: 1rem; max-height: 420px; overflow-y: auto;
        display: flex; flex-direction: column; gap: 0.875rem;
    }
    .chat-msg-group { display: flex; flex-direction: column; gap: 0.25rem; }
    .chat-speaker {
        font-family: 'JetBrains Mono', monospace; font-size: 0.6rem;
        color: var(--text3); letter-spacing: 0.08em; text-transform: uppercase; padding: 0 0.25rem;
    }
    .chat-bubble-user {
        background: var(--accent-dim); border: 1px solid rgba(47,111,235,0.2);
        border-radius: 14px 14px 4px 14px;
        padding: 0.65rem 1rem; font-size: 0.875rem; color: var(--text);
        margin-left: 2rem; line-height: 1.6; max-width: 85%;
        align-self: flex-end;
    }
    .chat-bubble-ai {
        background: var(--surface2); border: 1px solid var(--border);
        border-radius: 14px 14px 14px 4px;
        padding: 0.65rem 1rem; font-size: 0.875rem; color: var(--text2);
        margin-right: 2rem; line-height: 1.75; white-space: pre-wrap; max-width: 90%;
    }

    /* ═══════════════════════════════════════════════════
       PDF
    ═══════════════════════════════════════════════════ */
    .pdf-bar {
        display: flex; align-items: center; gap: 0.875rem;
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--r-lg); padding: 0.875rem 1.25rem; margin-bottom: 1.25rem;
    }
    .pdf-icon-wrap {
        width: 40px; height: 40px; background: var(--red-dim);
        border: 1px solid rgba(239,68,68,0.2); border-radius: var(--r-md);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; flex-shrink: 0;
    }
    .pdf-bar-name  { font-weight: 600; font-size: 0.88rem; color: var(--text); line-height: 1.3; }
    .pdf-bar-meta  { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--text3); margin-top: 2px; }
    .pdf-bar-badge {
        margin-left: auto; font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem; color: var(--green); background: var(--green-dim);
        padding: 3px 9px; border-radius: var(--r-full);
        border: 1px solid rgba(34,197,94,0.2); white-space: nowrap;
    }
    .pdf-dropzone {
        text-align: center; padding: 3.5rem 2rem;
        border: 2px dashed var(--border2); border-radius: var(--r-xl); margin-top: 1rem;
    }
    .pdf-dropzone-icon  { font-size: 2.5rem; margin-bottom: 0.875rem; opacity: 0.7; }
    .pdf-dropzone-title { font-weight: 600; font-size: 1rem; color: var(--text); margin-bottom: 0.4rem; }
    .pdf-dropzone-sub   { font-size: 0.83rem; color: var(--text3); max-width: 340px; margin: 0 auto; line-height: 1.6; }

    /* ═══════════════════════════════════════════════════
       AUTH
    ═══════════════════════════════════════════════════ */
    .auth-logo       { text-align: center; margin-bottom: 2rem; }
    .auth-logo-icon  { font-size: 2.25rem; margin-bottom: 0.5rem; }
    .auth-logo-title { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.04em; background: linear-gradient(135deg,#93c5fd,#60a5fa,#2f6feb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .auth-logo-sub   { font-size: 0.82rem; color: var(--text3); margin-top: 4px; }
    .auth-divider {
        display: flex; align-items: center; gap: 0.875rem;
        margin: 1.5rem 0; color: var(--text3); font-size: 0.75rem;
    }
    .auth-divider::before, .auth-divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }
    .auth-form-title { font-size: 1rem; font-weight: 600; color: var(--text); letter-spacing: -0.02em; margin-bottom: 1.25rem; }

    /* ═══════════════════════════════════════════════════
       COPY BUTTON
    ═══════════════════════════════════════════════════ */
    .copy-btn {
        background: var(--surface2); color: var(--text2);
        border: 1px solid var(--border2); border-radius: var(--r-md);
        font-family: 'Inter', sans-serif; font-weight: 500; font-size: 0.82rem;
        padding: 0.5rem 1rem; cursor: pointer; transition: all 0.15s;
        width: 100%; margin-top: 0.35rem;
    }
    .copy-btn:hover { background: var(--surface3); color: var(--text); border-color: var(--border3); }

    /* Voice hint */
    .voice-hint { font-size: 0.78rem; color: var(--text3); display: flex; align-items: center; gap: 0.4rem; }

    /* ═══════════════════════════════════════════════════
       TABLET ≤ 1024px
    ═══════════════════════════════════════════════════ */
    @media (max-width: 1024px) {
        .block-container { padding: 0.75rem 1rem 3rem !important; }
    }

    /* ═══════════════════════════════════════════════════
       MOBILE ≤ 640px
    ═══════════════════════════════════════════════════ */
    @media (max-width: 640px) {
        .hero { padding: 1rem 0; }
        .hero h1 { font-size: clamp(1.5rem, 7vw, 2rem); }
        .hero-sub { font-size: 0.85rem; }
        .content-box, .report-box { padding: 1rem; font-size: 0.83rem; }
        .chat-bubble-user { margin-left: 0.5rem; }
        .chat-bubble-ai   { margin-right: 0.5rem; }
        .metric-chip { min-width: 72px; padding: 0.75rem 0.6rem; }
        .metric-value { font-size: 1.2rem; }
        .stTabs [data-baseweb="tab-list"] { overflow-x: auto !important; flex-wrap: nowrap !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.75rem !important; padding: 0.32rem 0.7rem !important; white-space: nowrap !important; }
    }
    </style>
    """, unsafe_allow_html=True)