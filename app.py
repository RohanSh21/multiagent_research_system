import streamlit as st
import time
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

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    position: relative;
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

/* ── SEARCH BAR ── */
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
    cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

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
.step-card.active  { border-color: var(--accent);  }
.step-card.done    { border-color: #2e4a3b;          }
.step-card.error   { border-color: var(--danger);   }
.step-card.waiting { opacity: 0.45;                  }

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
.step-icon {
    font-size: 1.3rem;
    width: 2.2rem;
    text-align: center;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text);
}
.step-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.08em;
}
.badge {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-weight: 500;
    letter-spacing: 0.05em;
}
.badge-active  { background: rgba(79,255,176,0.15);  color: var(--accent);  }
.badge-done    { background: rgba(79,255,176,0.08);  color: #4fffb0aa;      }
.badge-waiting { background: rgba(107,114,128,0.12); color: var(--muted);   }
.badge-error   { background: rgba(248,113,113,0.15); color: var(--danger);  }

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
    font-family: 'DM Sans', sans-serif;
    font-size: 0.93rem;
    line-height: 1.75;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 500px;
    overflow-y: auto;
}
.content-box::-webkit-scrollbar { width: 5px; }
.content-box::-webkit-scrollbar-track { background: transparent; }
.content-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

.report-box {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.4rem;
    line-height: 1.85;
    font-size: 0.95rem;
}

/* ── METRICS ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
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

/* ── SIDEBAR ── */
.css-1d391kg, [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1.5px solid var(--border) !important;
}
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    color: var(--accent);
    letter-spacing: 0.02em;
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
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.history-item:hover { border-color: var(--accent); color: var(--text); }

/* ── PROGRESS / SPINNER ── */
.stProgress > div > div { background: var(--accent) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── STATUS MESSAGES ── */
.stAlert { border-radius: 10px !important; }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}
.streamlit-expanderContent {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0.0
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🧠 ResearchMind</div>', unsafe_allow_html=True)

    st.markdown("**Pipeline Agents**")
    agents_info = [
        ("🔍", "Search Agent",  "Tavily web search"),
        ("📄", "Reader Agent",  "Firecrawl scraper"),
        ("✍️", "Writer Chain",  "GPT / Claude LLM"),
        ("🔬", "Critic Chain",  "Quality reviewer"),
    ]
    for icon, name, desc in agents_info:
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
        '</div>',
        unsafe_allow_html=True,
    )

# ── Main layout ─────────────────────────────────────────────────────────────────
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
col_input, col_btn = st.columns([5, 1], gap="small")
with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025…",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("▶ Run", use_container_width=True)

st.markdown("")  # spacer

# ── Run pipeline ────────────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent",  "Discovering sources across the web",      "STEP 01"),
    ("📄", "Reader Agent",  "Scraping top URLs for deep content",       "STEP 02"),
    ("✍️", "Writer Chain",  "Synthesising research into a report",      "STEP 03"),
    ("🔬", "Critic Chain",  "Reviewing quality & completeness",         "STEP 04"),
]

def render_steps(active: int, done_set: set, error: int = -1):
    cols = st.columns(4, gap="small")
    for i, (icon, title, desc, label) in enumerate(STEPS):
        if i in done_set:
            cls, badge_cls, badge_txt = "done",    "badge-done",    "✓ DONE"
        elif i == active:
            cls, badge_cls, badge_txt = "active",  "badge-active",  "● RUNNING"
        elif i == error:
            cls, badge_cls, badge_txt = "error",   "badge-error",   "✗ ERROR"
        else:
            cls, badge_cls, badge_txt = "waiting", "badge-waiting", "○ WAITING"
        with cols[i]:
            st.markdown(f"""
            <div class="step-card {cls}">
                <div class="step-header">
                    <span class="step-icon">{icon}</span>
                    <div>
                        <div class="step-title">{title}</div>
                        <div class="step-meta">{label}</div>
                    </div>
                    <span class="badge {badge_cls}">{badge_txt}</span>
                </div>
                <div style="font-size:0.78rem;color:var(--muted);margin-top:0.4rem;line-height:1.4;">{desc}</div>
            </div>""", unsafe_allow_html=True)

if run_btn and topic.strip():
    st.session_state.result  = None
    st.session_state.running = True
    if topic.strip() not in st.session_state.history:
        st.session_state.history.append(topic.strip())

    step_placeholder = st.empty()
    progress_bar     = st.progress(0)
    status_msg       = st.empty()

    done_steps: set = set()
    start_time = time.time()
    error_idx  = -1

    try:
        # ── Visual step-by-step run ──────────────────────────────────────────
        with step_placeholder.container():
            render_steps(0, done_steps)
        status_msg.info("🔍  Search Agent is querying the web…")
        progress_bar.progress(10)

        # ---- Actual pipeline call (capture output) -------------------------
        # We run the full pipeline in one call; UI updates happen before/after.
        # For richer live feedback you could split into per-step calls.
        state = {}

        # Step 1 – search
        from agents import build_search_agent
        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"find recent, reliable and detailed information about: {topic.strip()}")]
        })
        state["search_results"] = search_result["messages"][-1].content
        done_steps.add(0)

        with step_placeholder.container():
            render_steps(1, done_steps)
        status_msg.info("📄  Reader Agent is scraping top resources…")
        progress_bar.progress(35)

        # Step 2 – reader
        from agents import build_reader_agent
        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic.strip()}', "
                f"pick the most important URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}")]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
        done_steps.add(1)

        with step_placeholder.container():
            render_steps(2, done_steps)
        status_msg.info("✍️  Writer is drafting the research report…")
        progress_bar.progress(60)

        # Step 3 – writer
        from agents import writer_chain
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic":    topic.strip(),
            "research": research_combined,
        })
        done_steps.add(2)

        with step_placeholder.container():
            render_steps(3, done_steps)
        status_msg.info("🔬  Critic is reviewing and scoring the report…")
        progress_bar.progress(85)

        # Step 4 – critic
        from agents import critic_chain
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        done_steps.add(3)

        elapsed = time.time() - start_time
        st.session_state.elapsed = elapsed
        st.session_state.result  = state

        with step_placeholder.container():
            render_steps(-1, done_steps)
        progress_bar.progress(100)
        status_msg.success(f"✅  Research complete in {elapsed:.1f}s")

    except Exception as exc:
        elapsed = time.time() - start_time
        with step_placeholder.container():
            render_steps(-1, done_steps, error_idx)
        progress_bar.progress(100)
        status_msg.error(f"❌  Pipeline error: {exc}")
        st.session_state.running = False

    st.session_state.running = False

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic before running.")

# ── Show idle step grid when no run ─────────────────────────────────────────────
if not st.session_state.running and st.session_state.result is None and not run_btn:
    render_steps(-1, set())


# ── Results ──────────────────────────────────────────────────────────────────────
result = st.session_state.result

if result:
    topic_display = st.session_state.history[-1] if st.session_state.history else "—"

    st.markdown("---")

    # Convert everything safely to string
    search_text = str(result.get("search_results", ""))
    scraped_text = str(result.get("scraped_content", ""))
    report_text = str(result.get("report", ""))
    feedback_text = str(result.get("feedback", ""))

    # Metrics row
    elapsed = st.session_state.elapsed

    search_words = len(search_text.split())
    scraped_words = len(scraped_text.split())
    report_words = len(report_text.split())

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-chip">
            <div class="metric-value">{elapsed:.1f}s</div>
            <div class="metric-label">Total Time</div>
        </div>

        <div class="metric-chip">
            <div class="metric-value">{search_words:,}</div>
            <div class="metric-label">Search Words</div>
        </div>

        <div class="metric-chip">
            <div class="metric-value">{scraped_words:,}</div>
            <div class="metric-label">Scraped Words</div>
        </div>

        <div class="metric-chip">
            <div class="metric-value">{report_words:,}</div>
            <div class="metric-label">Report Words</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab_report, tab_search, tab_scraped, tab_critic = st.tabs(
        [
            "📋 Final Report",
            "🔍 Search Results",
            "📄 Scraped Content",
            "🔬 Critic Feedback"
        ]
    )

    # Final Report
    with tab_report:

        st.markdown(
            f'<div class="report-box">{report_text}</div>',
            unsafe_allow_html=True,
        )

        st.download_button(
            label="⬇ Download Report (.txt)",
            data=report_text,
            file_name=f"research_{topic_display[:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

    # Search Results
    with tab_search:

        st.markdown(
            f'<div class="content-box">{search_text}</div>',
            unsafe_allow_html=True,
        )

    # Scraped Content
    with tab_scraped:

        st.markdown(
            f'<div class="content-box">{scraped_text}</div>',
            unsafe_allow_html=True,
        )

    # Critic Feedback
    with tab_critic:

        st.markdown(
            f'<div class="content-box">{feedback_text}</div>',
            unsafe_allow_html=True,
        )

    # Raw JSON Viewer
    with st.expander("🗂 Raw pipeline state (JSON)"):

        safe_result = {
            k: str(v)[:2000] + ("..." if len(str(v)) > 2000 else "")
            for k, v in result.items()
        }

        st.json(safe_result)