import streamlit as st
import time
import os
from components.voice_input import render_voice_input, inject_voice_listener
from auth.auth_logic import save_research
from auth.supabase_client import init_supabase


# ── LLM helper (original, untouched) ───────────────────────────────────────────
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


# ── Pipeline step renderer (original, untouched) ────────────────────────────────
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
                <div style="font-size:0.78rem;color:var(--muted);
                            margin-top:0.4rem;line-height:1.4;">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ── Pipeline runner (original + save to Supabase) ───────────────────────────────
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

        # Step 1 – Search
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user",
            f"find recent, reliable and detailed information about: {topic_str}")]})
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

        # Save to Supabase
        user = st.session_state.get("user")
        if user:
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

        status.success(f"✅  Research complete in {elapsed:.1f}s — saved to your history!")

    except Exception as exc:
        with step_ph.container(): render_steps(-1, done, -1)
        prog_bar.progress(100)
        status.error(f"❌  Pipeline error: {exc}")

    st.session_state.running = False


# ── Results renderer (original, untouched) ──────────────────────────────────────
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
                style="background:#18a689;border:none;border-radius:10px;
                       font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;
                       padding:0.55rem 1.4rem;cursor:pointer;width:100%;margin-top:0.3rem;">
                📋 Copy
            </button>""", unsafe_allow_html=True)

    with tab_search:
        st.markdown(f'<div class="content-box">{search_text}</div>', unsafe_allow_html=True)

    with tab_scraped:
        st.markdown(f'<div class="content-box">{scraped_text}</div>', unsafe_allow_html=True)

    with tab_critic:
        st.markdown(f'<div class="content-box">{feedback_text}</div>', unsafe_allow_html=True)

    # Follow-ups
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

    # Follow-up Chat
    st.markdown("---")
    st.markdown("""
    <div class="section-title">💬 Ask About This Report</div>
    <div class="section-sub">Summarise, explain, compare, or go deeper — just like ChatGPT</div>
    """, unsafe_allow_html=True)

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

    chat_col, send_col = st.columns([6, 1], gap="small")
    with chat_col:
        user_q = st.text_input(
            label="chat",
            placeholder="e.g. Summarise in 5 bullets… / What does this mean for India?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with send_col:
        send_btn = st.button("Send ➤", use_container_width=True)

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
        if st.button("🗑 Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

    with st.expander("🗂 Raw pipeline state (JSON)"):
        safe = {
            k: str(v)[:2000] + ("…" if len(str(v)) > 2000 else "")
            for k, v in result.items()
        }
        st.json(safe)


# ── Main research mode renderer ─────────────────────────────────────────────────
def render_research_mode():
    """Main entry point called from app.py."""

    inject_voice_listener()

    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-label">Multi-Agent Research System</div>
        <h1>DEEPDIVE AI</h1>
        <p class="hero-sub">
            Four specialised AI agents work in sequence — searching, scraping,
            writing and critiquing — to deliver deep research reports in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Input row
    col_input, col_run, col_regen = st.columns([5, 1, 1], gap="small")
    with col_input:
        topic = st.text_input(
            label="topic",
            placeholder="e.g.  Quantum computing breakthroughs in 2025…",
            label_visibility="collapsed",
            value=st.session_state.get("voice_topic", ""),
        )
    with col_run:
        run_btn = st.button("▶ Run", use_container_width=True)
    with col_regen:
        regen_btn = st.button(
            "🔄 Redo",
            use_container_width=True,
            disabled=(st.session_state.result is None),
        )

    # Voice row
    voice_col, hint_col = st.columns([3, 3], gap="small")
    with voice_col:
        render_voice_input()
    with hint_col:
        st.markdown(
            "🎤 **Voice Input** — Click the mic, speak your topic, "
            "then click **Use ➤** to auto-fill."
        )

    if st.session_state.get("voice_topic") and \
       topic == st.session_state.get("voice_topic"):
        st.session_state["voice_topic"] = ""

    st.markdown("")

    # Idle step grid
    if not st.session_state.running and \
       st.session_state.result is None and not run_btn:
        render_steps(-1, set())

    # Trigger pipeline
    if run_btn and topic.strip():
        run_pipeline(topic.strip())
    elif run_btn and not topic.strip():
        st.warning("Please enter a research topic before running.")

    if regen_btn and st.session_state.last_topic:
        run_pipeline(st.session_state.last_topic)

    # Show results
    render_results()