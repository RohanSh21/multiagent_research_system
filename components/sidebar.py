import streamlit as st
from datetime import datetime, timezone
from auth.auth_logic import delete_thread, logout_user
from components.model_selector import MODELS, DEFAULT_MODEL


def _group_threads(threads: list) -> dict:
    groups = {"Today": [], "Yesterday": [], "Last 7 Days": [], "Older": []}
    now = datetime.now(timezone.utc)
    for t in threads:
        try:
            created = datetime.fromisoformat(
                t["created_at"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)
        except Exception:
            groups["Older"].append(t)
            continue
        diff = (now - created).days
        if diff == 0:   groups["Today"].append(t)
        elif diff == 1: groups["Yesterday"].append(t)
        elif diff <= 7: groups["Last 7 Days"].append(t)
        else:           groups["Older"].append(t)
    return groups


def render_sidebar() -> None:

    # ── Brand ─────────────────────────────────────────────────────────
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-logo">
                <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <polygon points="16,2 28,9 28,23 16,30 4,23 4,9" fill="none" stroke="#2f6feb" stroke-width="1.5"/>
                    <polygon points="16,7 23,11 23,21 16,25 9,21 9,11" fill="rgba(47,111,235,0.15)" stroke="#60a5fa" stroke-width="1"/>
                    <circle cx="16" cy="16" r="3" fill="#2f6feb"/>
                    <line x1="16" y1="7" x2="16" y2="13" stroke="#60a5fa" stroke-width="1.2"/>
                    <line x1="16" y1="19" x2="16" y2="25" stroke="#60a5fa" stroke-width="1.2"/>
                    <line x1="23" y1="11" x2="18.6" y2="13.5" stroke="#60a5fa" stroke-width="1.2"/>
                    <line x1="13.4" y1="18.5" x2="9" y2="21" stroke="#60a5fa" stroke-width="1.2"/>
                    <line x1="9" y1="11" x2="13.4" y2="13.5" stroke="#60a5fa" stroke-width="1.2"/>
                    <line x1="18.6" y1="18.5" x2="23" y2="21" stroke="#60a5fa" stroke-width="1.2"/>
                </svg>
                <span style="background:linear-gradient(135deg,#93c5fd,#2f6feb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:700;letter-spacing:-0.02em;">Nexus AI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── User row ───────────────────────────────────────────────────────
    is_guest  = st.session_state.get("is_guest", False)
    user      = st.session_state.get("user") or {}
    user_name = "Guest" if is_guest else user.get("full_name", "User")
    initials  = "G" if is_guest else user_name[0].upper()

    st.markdown(f"""
        <div class="sidebar-user-row">
            <div class="sidebar-avatar">{initials}</div>
            <span class="sidebar-username">{user_name}</span>
        </div>
    """, unsafe_allow_html=True)

    if is_guest:
        st.markdown(
            '<div class="guest-banner">⚡ Guest mode — sign in to save history</div>',
            unsafe_allow_html=True,
        )

    # ── Sign out ───────────────────────────────────────────────────────
    if st.button("↩  Sign out", key="logout_btn", use_container_width=True):
        logout_user()
        st.session_state["is_guest"] = False
        st.rerun()

    st.markdown("---")

    # ── New Research ───────────────────────────────────────────────────
    if st.button("＋  New Research", use_container_width=True,
                 type="primary", key="new_research_btn"):
        st.session_state.update({
            "result": None, "active_thread": None,
            "last_topic": "", "chat_messages": [],
            "followups": [], "active_mode": "research",
        })
        st.rerun()

    # ── Mode nav ───────────────────────────────────────────────────────
    active_mode = st.session_state.get("active_mode", "research")
    m1, m2 = st.columns(2, gap="small")
    with m1:
        if st.button("🔍 Research", use_container_width=True,
                     type="primary" if active_mode == "research" else "secondary",
                     key="sidebar_research"):
            st.session_state.active_mode = "research"
            st.rerun()
    with m2:
        if st.button("📄 PDF", use_container_width=True,
                     type="primary" if active_mode == "rag" else "secondary",
                     key="sidebar_rag"):
            st.session_state.active_mode = "rag"
            st.rerun()

    st.markdown("---")

    # ── Model selector ─────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">Model</div>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        label="model", options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(
            st.session_state.get("selected_model_label", DEFAULT_MODEL)
        ),
        label_visibility="collapsed", key="selected_model_name",
    )
    model_info = MODELS[selected_model]
    st.session_state["selected_model_id"]    = model_info["id"]
    st.session_state["selected_model_label"] = selected_model
    st.markdown(f"""
        <div class="model-badge">
            <div class="model-badge-dot"></div>
            {model_info['badge']}
            <span style="color:var(--text3);margin-left:2px;">{model_info['use_case']}</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Agents ─────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-section-label">Agents</div>', unsafe_allow_html=True)
    for icon, name, desc in [
        ("🔍", "Search",  "Tavily web search"),
        ("📄", "Reader",  "Firecrawl scraper"),
        ("✍️", "Writer",  "Mistral LLM"),
        ("🔬", "Critic",  "Quality reviewer"),
    ]:
        st.markdown(f"""
            <div class="agent-chip">
                <div class="agent-dot"></div>
                <div>
                    <div class="agent-name">{icon} {name}</div>
                    <div class="agent-desc">{desc}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Thread history ─────────────────────────────────────────────────
    threads = st.session_state.get("threads", [])
    active  = st.session_state.get("active_thread")

    if is_guest:
        st.markdown(
            '<div style="font-size:0.78rem;color:var(--text3);text-align:center;'
            'padding:0.75rem 0;">Sign in to view history</div>',
            unsafe_allow_html=True,
        )
    elif threads:
        st.markdown('<div class="sidebar-section-label">History</div>', unsafe_allow_html=True)
        groups = _group_threads(threads)
        for group_name, group_threads in groups.items():
            if not group_threads:
                continue
            st.markdown(
                f'<div class="thread-group-label">{group_name}</div>',
                unsafe_allow_html=True,
            )
            for thread in group_threads:
                tid       = thread["id"]
                title     = thread.get("title") or thread.get("topic", "Untitled")
                title     = title[:30] + "…" if len(title) > 30 else title
                is_active = (active == tid)
                t_col, d_col = st.columns([5, 1], gap="small")
                with t_col:
                    if st.button(title, key=f"thread_{tid}",
                                 use_container_width=True,
                                 type="primary" if is_active else "secondary"):
                        st.session_state.update({
                            "active_thread": tid,
                            "result": {
                                "report":          thread.get("report", ""),
                                "search_results":  thread.get("search_results", ""),
                                "scraped_content": "",
                                "feedback":        thread.get("feedback", ""),
                            },
                            "last_topic":    thread.get("topic", ""),
                            "chat_messages": [],
                            "followups":     [],
                            "active_mode":   "research",
                        })
                        st.rerun()
                with d_col:
                    if st.button("🗑", key=f"del_{tid}", help="Delete"):
                        delete_thread(tid)
                        st.session_state["threads"] = [
                            t for t in threads if t["id"] != tid
                        ]
                        if active == tid:
                            st.session_state["active_thread"] = None
                            st.session_state["result"]        = None
                        st.rerun()
    else:
        st.markdown(
            '<div style="font-size:0.78rem;color:var(--text3);text-align:center;'
            'padding:0.75rem 0;">No history yet</div>',
            unsafe_allow_html=True,
        )

    # ── Footer ─────────────────────────────────────────────────────────
    st.markdown(
        '<div class="sidebar-footer">v1.0 · LangGraph + Supabase</div>',
        unsafe_allow_html=True,
    )