import streamlit as st
import time
import os
from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
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

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

.hero { text-align: center; padding: 3.5rem 1rem 2.5rem; }
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
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

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
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled { opacity: 0.35 !important; cursor: not-allowed !important; }

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
.step-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.3rem; }
.step-icon { font-size: 1.3rem; width: 2.2rem; text-align: center; }
.step-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; color: var(--text); }
.step-meta { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: var(--muted); letter-spacing: 0.08em; }
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
.stTabs [aria-selected="true"] { background: var(--surface2) !important; color: var(--text) !important; }

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
.content-box::-webkit-scrollbar { width: 5px; }
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

.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-chip {
    flex: 1;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-value { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; color: var(--accent); }
.metric-label { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.15rem; }

/* ── FOLLOW-UP CHIPS ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
    margin-bottom: 0.2rem;
}
.section-sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 1rem; }

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
.chat-container::-webkit-scrollbar { width: 5px; }
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

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
.stProgress > div > div { background: var(--accent) !important; }
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

# ── Session state ───────────────────────────────────────────────────────────────
for key, default in {
    "history":        [],
    "result":         None,
    "running":        False,
    "elapsed":        0.0,
    "last_topic":     "",
    "followups":      [],
    "chat_messages":  [],
    # RAG state
    "rag_pdf_text":   "",
    "rag_pdf_name":   "",
    "rag_messages":   [],
    "active_mode":    "research",   # "research" | "rag"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── LLM helper ─────────────────────────────────────────────────────────────────
def call_llm(prompt: str) -> str:
    try:
        from langchain_mistralai import ChatMistralAI
        llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=0.4,
        )
        return llm.invoke(prompt).content
    except Exception as e:
        return f"Error: {str(e)}"

def extract_pdf_text(uploaded_file) -> str:
    """Extract plain text from an uploaded PDF using pypdf."""
    try:
        import pypdf, io
        reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
        pages  = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    except Exception as e:
        return f"ERROR_READING_PDF: {str(e)}"

def generate_followups(topic: str, report: str) -> list:
    prompt = (
        f"Based on this research report about '{topic}', generate exactly 3 short, "
        f"interesting follow-up questions a curious reader would ask next. "
        f"Return ONLY the 3 questions, one per line, no numbering, no extra text.\n\n"
        f"Report (first 800 chars):\n{report[:800]}"
    )
    raw = call_llm(prompt)
    return [q.strip() for q in raw.strip().split("\n") if q.strip()][:3]

# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🧠 ResearchMind</div>', unsafe_allow_html=True)

    # ── Mode switcher ──────────────────────────────────────────────────────
    st.markdown("**Mode**")
    mode_col1, mode_col2 = st.columns(2, gap="small")
    with mode_col1:
        if st.button("🔍 Research", use_container_width=True,
                     type="primary" if st.session_state.active_mode == "research" else "secondary"):
            st.session_state.active_mode = "research"
            st.rerun()
    with mode_col2:
        if st.button("📄 PDF Chat", use_container_width=True,
                     type="primary" if st.session_state.active_mode == "rag" else "secondary"):
            st.session_state.active_mode = "rag"
            st.rerun()

    st.markdown("---")
    st.markdown("**Pipeline Agents**")
    for icon, name, desc in [
        ("🔍", "Search Agent", "Tavily web search"),
        ("📄", "Reader Agent", "Firecrawl scraper"),
        ("✍️", "Writer Chain", "Mistral LLM"),
        ("🔬", "Critic Chain", "Quality reviewer"),
    ]:
        st.markdown(f"""
        <div class="step-card done" style="padding:0.8rem 1rem;margin-bottom:0.5rem;">
            <div class="step-header" style="margin-bottom:0;">
                <span class="step-icon" style="font-size:1rem;">{icon}</span>
                <div>
                    <div class="step-title" style="font-size:0.85rem;">{name}</div>
                    <div class="step-meta">{desc}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.history:
        st.markdown("**Recent Searches**")
        for h in reversed(st.session_state.history[-6:]):
            st.markdown(f'<div class="history-item">📌 {h}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:#6b7280;">'
        'Multi-Agent Research System<br>v1.0 · LangGraph + LangChain'
        '</div>', unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════════════════════════
# ── RAG MODE ────────────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.active_mode == "rag":

    st.markdown("""
    <div class="hero">
        <div class="hero-label">PDF Intelligence</div>
        <h1>PDF Chat</h1>
        <p class="hero-sub">
            Upload any PDF — research paper, report, contract, book —
            and ask questions about it in plain English.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Upload zone
    uploaded = st.file_uploader(
        label="Upload a PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help="Max ~50 pages works best",
    )

    if uploaded:
        if uploaded.name != st.session_state.rag_pdf_name:
            # New file — extract text
            with st.spinner("📖  Reading PDF…"):
                text = extract_pdf_text(uploaded)
            if text.startswith("ERROR_READING_PDF"):
                st.error(f"Could not read PDF: {text}")
            else:
                st.session_state.rag_pdf_text = text
                st.session_state.rag_pdf_name = uploaded.name
                st.session_state.rag_messages = []
                st.success(f"✅  **{uploaded.name}** loaded — {len(text.split()):,} words extracted.")

    if st.session_state.rag_pdf_name:
        # PDF info bar
        st.markdown(f"""
        <div style="background:var(--surface);border:1.5px solid var(--border);border-radius:12px;
                    padding:0.9rem 1.3rem;display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;">
            <span style="font-size:1.4rem;">📄</span>
            <div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;color:var(--text);">
                    {st.session_state.rag_pdf_name}
                </div>
                <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--muted);">
                    {len(st.session_state.rag_pdf_text.split()):,} words · ready to chat
                </div>
            </div>
            <div style="margin-left:auto;font-family:'DM Mono',monospace;font-size:0.7rem;
                        color:var(--accent);background:rgba(79,255,176,0.1);
                        padding:0.2rem 0.7rem;border-radius:999px;">● LOADED</div>
        </div>
        """, unsafe_allow_html=True)

        # Suggested starter questions
        starters = [
            "Summarise this document in 5 bullet points",
            "What are the key findings?",
            "What conclusions does this document reach?",
        ]
        st.markdown("""
        <div class="section-title">💡 Quick Questions</div>
        <div class="section-sub">Click to ask instantly</div>
        """, unsafe_allow_html=True)

        s_cols = st.columns(3, gap="small")
        for i, q in enumerate(starters):
            with s_cols[i]:
                if st.button(q, key=f"rag_starter_{i}", use_container_width=True):
                    st.session_state.rag_messages.append({"role": "user", "content": q})
                    ctx = st.session_state.rag_pdf_text[:4000]
                    with st.spinner("Thinking…"):
                        ans = call_llm(
                            f"You are a helpful assistant. Answer based ONLY on the document below.\n\n"
                            f"DOCUMENT:\n{ctx}\n\nQuestion: {q}\n\nAnswer clearly."
                        )
                    st.session_state.rag_messages.append({"role": "ai", "content": ans})
                    st.rerun()

        # Chat history
        st.markdown("---")
        st.markdown("""
        <div class="section-title">💬 Chat with your PDF</div>
        <div class="section-sub">Ask anything about the document</div>
        """, unsafe_allow_html=True)

        if st.session_state.rag_messages:
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.rag_messages:
                if msg["role"] == "user":
                    chat_html += (
                        f'<div class="chat-msg">'
                        f'<div class="chat-label">YOU</div>'
                        f'<div class="chat-msg-user">{msg["content"]}</div>'
                        f'</div>'
                    )
                else:
                    chat_html += (
                        f'<div class="chat-msg">'
                        f'<div class="chat-label">RESEARCHMIND</div>'
                        f'<div class="chat-msg-ai">{msg["content"]}</div>'
                        f'</div>'
                    )
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

        # Input row
        rag_col, rag_send = st.columns([6, 1], gap="small")
        with rag_col:
            rag_q = st.text_input(
                label="rag_chat",
                placeholder="e.g. What methodology was used? / List all recommendations / Who are the authors?",
                label_visibility="collapsed",
                key="rag_input",
            )
        with rag_send:
            rag_send_btn = st.button("Send ➤", use_container_width=True, key="rag_send")

        if rag_send_btn and rag_q.strip():
            st.session_state.rag_messages.append({"role": "user", "content": rag_q.strip()})
            # Use last 4000 chars of PDF + last 6 chat turns as context
            doc_ctx      = st.session_state.rag_pdf_text[:4000]
            history_ctx  = "\n".join(
                [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.rag_messages[-6:]]
            )
            with st.spinner("Thinking…"):
                ans = call_llm(
                    f"You are a helpful assistant. Answer based ONLY on the document below.\n\n"
                    f"DOCUMENT:\n{doc_ctx}\n\n"
                    f"Conversation so far:\n{history_ctx}\n\n"
                    f"User: {rag_q.strip()}\n\nAnswer clearly and helpfully."
                )
            st.session_state.rag_messages.append({"role": "ai", "content": ans})
            st.rerun()

        col_clear, col_new = st.columns([1, 1], gap="small")
        with col_clear:
            if st.session_state.rag_messages:
                if st.button("🗑 Clear Chat", key="rag_clear"):
                    st.session_state.rag_messages = []
                    st.rerun()
        with col_new:
            if st.button("📂 Load New PDF", key="rag_new"):
                st.session_state.rag_pdf_text = ""
                st.session_state.rag_pdf_name = ""
                st.session_state.rag_messages = []
                st.rerun()

    else:
        # No PDF uploaded yet — show placeholder
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;border:2px dashed var(--border);
                    border-radius:16px;margin-top:1rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;
                        color:var(--text);margin-bottom:0.5rem;">Drop your PDF above</div>
            <div style="color:var(--muted);font-size:0.88rem;max-width:360px;margin:0 auto;">
                Research papers, contracts, books, reports — upload any PDF and
                start asking questions instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()   # Don't render Research mode below

# ── RESEARCH MODE ────────────────────────────────────────────────────────────────

# ── Hero ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">Multi-Agent Research System</div>
    <h1>ResearchMind AI</h1>
    <p class="hero-sub">
        Four specialised AI agents work in sequence — searching, scraping,
        writing and critiquing — to deliver deep research reports in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input row ───────────────────────────────────────────────────────────────────
col_input, col_run, col_regen = st.columns([5, 1, 1], gap="small")
with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025…",
        label_visibility="collapsed",
    )
with col_run:
    run_btn = st.button("▶ Run", use_container_width=True)
with col_regen:
    regen_btn = st.button(
        "🔄 Redo",
        use_container_width=True,
        disabled=(st.session_state.result is None),
    )

st.markdown("")

# ── Step renderer ───────────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent",  "Discovering sources across the web",  "STEP 01"),
    ("📄", "Reader Agent",  "Scraping top URLs for deep content",  "STEP 02"),
    ("✍️", "Writer Chain",  "Synthesising research into a report", "STEP 03"),
    ("🔬", "Critic Chain",  "Reviewing quality & completeness",    "STEP 04"),
]

def render_steps(active: int, done_set: set, error: int = -1):
    cols = st.columns(4, gap="small")
    for i, (icon, title, desc, label) in enumerate(STEPS):
        if i in done_set:
            cls, bc, bt = "done",    "badge-done",    "✓ DONE"
        elif i == active:
            cls, bc, bt = "active",  "badge-active",  "● RUNNING"
        elif i == error:
            cls, bc, bt = "error",   "badge-error",   "✗ ERROR"
        else:
            cls, bc, bt = "waiting", "badge-waiting", "○ WAITING"
        with cols[i]:
            st.markdown(f"""
            <div class="step-card {cls}">
                <div class="step-header">
                    <span class="step-icon">{icon}</span>
                    <div>
                        <div class="step-title">{title}</div>
                        <div class="step-meta">{label}</div>
                    </div>
                    <span class="badge {bc}">{bt}</span>
                </div>
                <div style="font-size:0.78rem;color:var(--muted);margin-top:0.4rem;line-height:1.4;">{desc}</div>
            </div>""", unsafe_allow_html=True)

# ── Pipeline runner ─────────────────────────────────────────────────────────────
def run_pipeline(topic_str: str):
    st.session_state.result        = None
    st.session_state.followups     = []
    st.session_state.chat_messages = []
    st.session_state.running       = True

    if topic_str not in st.session_state.history:
        st.session_state.history.append(topic_str)

    step_ph  = st.empty()
    prog_bar = st.progress(0)
    status   = st.empty()
    done: set = set()
    start = time.time()

    try:
        with step_ph.container(): render_steps(0, done)
        status.info("🔍  Search Agent is querying the web…")
        prog_bar.progress(10)

        from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
        state = {}

        # Step 1 – Search
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user", f"find recent, reliable and detailed information about: {topic_str}")]})
        state["search_results"] = sr["messages"][-1].content
        done.add(0)

        with step_ph.container(): render_steps(1, done)
        status.info("📄  Reader Agent is scraping top resources…")
        prog_bar.progress(35)

        # Step 2 – Reader
        ra = build_reader_agent()
        rr = ra.invoke({"messages": [("user",
            f"Based on the following search results about '{topic_str}', "
            f"pick the most important URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}")]})
        state["scraped_content"] = rr["messages"][-1].content
        done.add(1)

        with step_ph.container(): render_steps(2, done)
        status.info("✍️  Writer is drafting the research report…")
        prog_bar.progress(60)

        # Step 3 – Writer
        combined = (f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}")
        state["report"] = writer_chain.invoke({"topic": topic_str, "research": combined})
        done.add(2)

        with step_ph.container(): render_steps(3, done)
        status.info("🔬  Critic is reviewing and scoring the report…")
        prog_bar.progress(85)

        # Step 4 – Critic
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        done.add(3)

        elapsed = time.time() - start
        st.session_state.elapsed    = elapsed
        st.session_state.result     = state
        st.session_state.last_topic = topic_str

        with step_ph.container(): render_steps(-1, done)
        prog_bar.progress(100)
        status.info("💡  Generating follow-up suggestions…")

        st.session_state.followups = generate_followups(topic_str, str(state["report"]))
        status.success(f"✅  Research complete in {elapsed:.1f}s — ready to explore!")

    except Exception as exc:
        with step_ph.container(): render_steps(-1, done, -1)
        prog_bar.progress(100)
        status.error(f"❌  Pipeline error: {exc}")

    st.session_state.running = False

# ── Trigger ─────────────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    run_pipeline(topic.strip())
elif run_btn and not topic.strip():
    st.warning("Please enter a research topic before running.")

if regen_btn and st.session_state.last_topic:
    run_pipeline(st.session_state.last_topic)

if not st.session_state.running and st.session_state.result is None and not run_btn:
    render_steps(-1, set())

# ── Results ──────────────────────────────────────────────────────────────────────
result = st.session_state.result

if result:
    topic_display = st.session_state.last_topic or "research"
    report_text   = str(result.get("report", ""))
    search_text   = str(result.get("search_results", ""))
    scraped_text  = str(result.get("scraped_content", ""))
    feedback_text = str(result.get("feedback", ""))

    st.markdown("---")

    # Metrics
    elapsed = st.session_state.elapsed
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-chip">
            <div class="metric-value">{elapsed:.1f}s</div>
            <div class="metric-label">Total Time</div>
        </div>
        <div class="metric-chip">
            <div class="metric-value">{len(search_text.split()):,}</div>
            <div class="metric-label">Search Words</div>
        </div>
        <div class="metric-chip">
            <div class="metric-value">{len(scraped_text.split()):,}</div>
            <div class="metric-label">Scraped Words</div>
        </div>
        <div class="metric-chip">
            <div class="metric-value">{len(report_text.split()):,}</div>
            <div class="metric-label">Report Words</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab_report, tab_search, tab_scraped, tab_critic = st.tabs(
        ["📋 Final Report", "🔍 Search Results", "📄 Scraped Content", "🔬 Critic Feedback"]
    )

    with tab_report:
        st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
        dl_col, cp_col = st.columns([2, 1], gap="small")
        with dl_col:
            st.download_button(
                label="⬇ Download Report (.txt)",
                data=report_text,
                file_name=f"research_{topic_display[:40].replace(' ','_')}.txt",
                mime="text/plain",
            )
        with cp_col:
            safe_report = report_text[:3000].replace("`", "'").replace("\n", "\\n")
            st.markdown(f"""
            <button onclick="navigator.clipboard.writeText(`{safe_report}`);
                            this.innerText='✅ Copied!';
                            setTimeout(()=>this.innerText='📋 Copy',2000)"
                style="background:linear-gradient(135deg,#4fffb0,#38bdf8);color:#0a0b0f;
                       border:none;border-radius:10px;font-family:Syne,sans-serif;
                       font-weight:700;font-size:0.9rem;padding:0.55rem 1.4rem;
                       cursor:pointer;width:100%;margin-top:0.3rem;">
                📋 Copy
            </button>""", unsafe_allow_html=True)

    with tab_search:
        st.markdown(f'<div class="content-box">{search_text}</div>', unsafe_allow_html=True)

    with tab_scraped:
        st.markdown(f'<div class="content-box">{scraped_text}</div>', unsafe_allow_html=True)

    with tab_critic:
        st.markdown(f'<div class="content-box">{feedback_text}</div>', unsafe_allow_html=True)

    # ── ✨ FEATURE 1: Suggested Follow-ups ────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="section-title">💡 Suggested Follow-ups</div>
    <div class="section-sub">Click any question to get an instant answer</div>
    """, unsafe_allow_html=True)

    followups = st.session_state.followups
    if followups:
        fu_cols = st.columns(len(followups), gap="small")
        for i, q in enumerate(followups):
            with fu_cols[i]:
                if st.button(q, key=f"fu_{i}", use_container_width=True):
                    st.session_state.chat_messages.append({"role": "user", "content": q})
                    with st.spinner("Thinking…"):
                        answer = call_llm(
                            f"You are a research assistant. The user read a report about '{topic_display}'.\n"
                            f"Report (first 1200 chars):\n{report_text[:1200]}\n\n"
                            f"Question: {q}\n\nAnswer clearly and concisely."
                        )
                    st.session_state.chat_messages.append({"role": "ai", "content": answer})
                    st.rerun()
    else:
        st.markdown(
            '<p style="color:var(--muted);font-size:0.85rem;">No suggestions generated yet.</p>',
            unsafe_allow_html=True,
        )

    # ── ✨ FEATURE 2 & 3: Follow-up Chat ──────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="section-title">💬 Ask About This Report</div>
    <div class="section-sub">Summarise, explain, compare, or go deeper — just like ChatGPT</div>
    """, unsafe_allow_html=True)

    # Render chat history
    if st.session_state.chat_messages:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                chat_html += (
                    f'<div class="chat-msg">'
                    f'<div class="chat-label">YOU</div>'
                    f'<div class="chat-msg-user">{msg["content"]}</div>'
                    f'</div>'
                )
            else:
                chat_html += (
                    f'<div class="chat-msg">'
                    f'<div class="chat-label">RESEARCHMIND</div>'
                    f'<div class="chat-msg-ai">{msg["content"]}</div>'
                    f'</div>'
                )
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

    # Chat input row
    chat_col, send_col = st.columns([6, 1], gap="small")
    with chat_col:
        user_q = st.text_input(
            label="chat",
            placeholder="e.g. Summarise in 5 bullets… / What does this mean for India? / Who are the key players?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with send_col:
        send_btn = st.button("Send ➤", use_container_width=True)

    if send_btn and user_q.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_q.strip()})
        history_ctx = "\n".join(
            [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.chat_messages[-6:]]
        )
        with st.spinner("Thinking…"):
            answer = call_llm(
                f"You are a research assistant. The user read a report about '{topic_display}'.\n"
                f"Report (first 1500 chars):\n{report_text[:1500]}\n\n"
                f"Conversation so far:\n{history_ctx}\n\n"
                f"User: {user_q.strip()}\n\nAnswer clearly and helpfully."
            )
        st.session_state.chat_messages.append({"role": "ai", "content": answer})
        st.rerun()

    if st.session_state.chat_messages:
        if st.button("🗑 Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

    # Raw JSON expander
    with st.expander("🗂 Raw pipeline state (JSON)"):
        safe = {k: str(v)[:2000] + ("…" if len(str(v)) > 2000 else "") for k, v in result.items()}
        st.json(safe)