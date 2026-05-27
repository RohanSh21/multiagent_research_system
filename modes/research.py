import streamlit as st
import time
import os
from components.voice_input import render_voice_input, inject_voice_listener
from auth.auth_logic import save_research
from auth.supabase_client import init_supabase


# ── LLM helper ────────────────────────────────────────────────────────────────
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


def generate_followups(topic: str, report: str) -> list:
    prompt = (
        f"Based on this research report about '{topic}', generate exactly 3 short, "
        f"interesting follow-up questions a curious reader would ask next. "
        f"Return ONLY the 3 questions, one per line, no numbering, no extra text.\n\n"
        f"Report (first 800 chars):\n{report[:800]}"
    )
    raw = call_llm(prompt)
    return [q.strip() for q in raw.strip().split("\n") if q.strip()][:3]


# ── Pipeline steps ────────────────────────────────────────────────────────────
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
            cls, bc, bt = "done",    "badge-done",    "✓ Done"
        elif i == active:
            cls, bc, bt = "active",  "badge-active",  "● Running"
        elif i == error:
            cls, bc, bt = "error",   "badge-error",   "✗ Error"
        else:
            cls, bc, bt = "waiting", "badge-waiting", "○ Waiting"
        with cols[i]:
            st.markdown(f"""
            <div class="step-card {cls}">
                <div class="step-header">
                    <div class="step-icon-wrap">{icon}</div>
                    <div style="flex:1;min-width:0;">
                        <div class="step-title">{title}</div>
                        <div class="step-label">{label}</div>
                    </div>
                    <span class="step-badge {bc}">{bt}</span>
                </div>
                <div class="step-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ── Pipeline runner ───────────────────────────────────────────────────────────
def run_pipeline(topic_str: str):
    st.session_state.result        = None
    st.session_state.followups     = []
    st.session_state.chat_messages = []
    st.session_state.running       = True
    st.session_state.active_thread = None

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

        # Step 1
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user",
            f"find recent, reliable and detailed information about: {topic_str}")]})
        state["search_results"] = sr["messages"][-1].content
        done.add(0)

        with step_ph.container(): render_steps(1, done)
        status.info("📄  Reader Agent is scraping top resources…")
        prog_bar.progress(35)

        # Step 2
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

        # Step 3
        combined = (f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}")
        state["report"] = writer_chain.invoke({"topic": topic_str, "research": combined})
        done.add(2)

        with step_ph.container(): render_steps(3, done)
        status.info("🔬  Critic is reviewing and scoring the report…")
        prog_bar.progress(85)

        # Step 4
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

        user     = st.session_state.get("user")
        is_guest = st.session_state.get("is_guest", False)
        if user and not is_guest:
            save_research(
                user_id        = user["id"],
                topic          = topic_str,
                report         = str(state["report"]),
                search_results = str(state["search_results"]),
                feedback       = str(state["feedback"]),
            )
            supabase   = init_supabase()
            new_thread = supabase.table("research_history").select(
                "id, topic, title, report, search_results, feedback, created_at"
            ).eq("user_id", user["id"]).order("created_at", desc=True).limit(1).execute()
            if new_thread.data:
                st.session_state["threads"] = (
                    new_thread.data + st.session_state.get("threads", [])
                )
            status.success(f"✅  Research complete in {elapsed:.1f}s — saved to history!")
        else:
            status.success(f"✅  Research complete in {elapsed:.1f}s!")

    except Exception as exc:
        with step_ph.container(): render_steps(-1, done, -1)
        prog_bar.progress(100)
        status.error(f"❌  Pipeline error: {exc}")

    st.session_state.running = False


# ── Results ───────────────────────────────────────────────────────────────────
def render_results():
    result = st.session_state.result
    if not result:
        return

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
        ["📋 Report", "🔍 Search Results", "📄 Scraped", "🔬 Critic"]
    )

    with tab_report:
        st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        dl_col, cp_col = st.columns([2, 1], gap="small")
        with dl_col:
            st.download_button(
                label="⬇  Download Report (.txt)",
                data=report_text,
                file_name=f"research_{topic_display[:40].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with cp_col:
            safe_report = report_text[:3000].replace("`", "'").replace("\n", "\\n")
            st.markdown(f"""
            <button class="copy-btn"
                onclick="navigator.clipboard.writeText(`{safe_report}`);
                         this.innerText='✅ Copied!';
                         setTimeout(()=>this.innerText='📋 Copy',2000)">
                📋 Copy
            </button>""", unsafe_allow_html=True)

    with tab_search:
        st.markdown(f'<div class="content-box">{search_text}</div>', unsafe_allow_html=True)

    with tab_scraped:
        st.markdown(f'<div class="content-box">{scraped_text}</div>', unsafe_allow_html=True)

    with tab_critic:
        st.markdown(f'<div class="content-box">{feedback_text}</div>', unsafe_allow_html=True)

    # Follow-ups
    st.markdown("""
    <div class="section-header">
        <div class="section-title">💡 Suggested follow-ups</div>
        <div class="section-sub">Click any question to get an instant answer</div>
    </div>
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

    # Chat
    st.markdown("""
    <div class="section-header">
        <div class="section-title">💬 Ask about this report</div>
        <div class="section-sub">Summarise, explain, compare, or go deeper</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.chat_messages:
        msgs_html = ""
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                msgs_html += f"""
                <div class="chat-msg-group">
                    <div class="chat-speaker">You</div>
                    <div class="chat-bubble-user">{msg["content"]}</div>
                </div>"""
            else:
                msgs_html += f"""
                <div class="chat-msg-group">
                    <div class="chat-speaker">Nexus AI</div>
                    <div class="chat-bubble-ai">{msg["content"]}</div>
                </div>"""
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="chat-messages">{msgs_html}</div>
        </div>
        """, unsafe_allow_html=True)

    chat_col, send_col = st.columns([6, 1], gap="small")
    with chat_col:
        user_q = st.text_input(
            label="chat", placeholder="Ask anything about this report…",
            label_visibility="collapsed", key="chat_input",
        )
    with send_col:
        send_btn = st.button("Send", use_container_width=True, type="primary")

    if send_btn and user_q.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_q.strip()})
        history_ctx = "\n".join(
            [f"{m['role'].upper()}: {m['content']}"
             for m in st.session_state.chat_messages[-6:]]
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
        if st.button("🗑  Clear chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

    with st.expander("🔧 Raw pipeline output"):
        safe = {
            k: str(v)[:2000] + ("…" if len(str(v)) > 2000 else "")
            for k, v in result.items()
        }
        st.json(safe)


# ── Entry point ───────────────────────────────────────────────────────────────
def render_research_mode():
    inject_voice_listener()

    is_guest = st.session_state.get("is_guest", False)

    if is_guest:
        st.markdown("""
        <div class="guest-banner">
            ⚡ You're in guest mode — research won't be saved.
            <a href="#" style="color:#93c5fd;margin-left:4px;">Sign in for full access.</a>
        </div>
        """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">⚡ Multi-Agent Research System</div>
        <h1>Research anything,<br><em>instantly.</em></h1>
        <p class="hero-sub">
            Four AI agents search, scrape, write, and critique —
            delivering deep research reports in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Input row
    col_input, col_run, col_regen = st.columns([5, 1, 1], gap="small")
    with col_input:
        topic = st.text_input(
            label="topic",
            placeholder="What do you want to research?",
            label_visibility="collapsed",
            value=st.session_state.get("voice_topic", ""),
        )
    with col_run:
        run_btn = st.button("▶  Run", use_container_width=True, type="primary")
    with col_regen:
        regen_btn = st.button(
            "↺  Redo", use_container_width=True,
            disabled=(st.session_state.result is None),
        )

    # Voice row
    v1, v2 = st.columns([3, 3], gap="small")
    with v1:
        render_voice_input()
    with v2:
        st.markdown(
            '<div class="voice-hint">🎤 Click mic → speak → click Use ➤</div>',
            unsafe_allow_html=True,
        )

    if st.session_state.get("voice_topic") and topic == st.session_state.get("voice_topic"):
        st.session_state["voice_topic"] = ""

    st.markdown("")

    # Idle step grid
    if not st.session_state.running and st.session_state.result is None and not run_btn:
        render_steps(-1, set())

    # Triggers
    if run_btn and topic.strip():
        run_pipeline(topic.strip())
    elif run_btn and not topic.strip():
        st.warning("Please enter a research topic.")

    if regen_btn and st.session_state.last_topic:
        run_pipeline(st.session_state.last_topic)

    render_results()