import streamlit as st
from datetime import datetime, timezone
from auth.auth_logic import delete_thread, logout_user
from components.model_selector import MODELS, DEFAULT_MODEL


def _group_threads(threads: list) -> dict:
    """Group threads by Today / Yesterday / Last 7 Days / Older."""
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
        if diff == 0:        groups["Today"].append(t)
        elif diff == 1:      groups["Yesterday"].append(t)
        elif diff <= 7:      groups["Last 7 Days"].append(t)
        else:                groups["Older"].append(t)
    return groups


def render_sidebar() -> None:
    """Renders full sidebar — brand, user, threads, model selector, agents."""

    with st.sidebar:

        # ── Brand ─────────────────────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-brand">🧠 ResearchMind</div>',
            unsafe_allow_html=True,
        )

        # ── User info + logout ─────────────────────────────────────────────
        user      = st.session_state.get("user", {})
        user_name = user.get("full_name", "User")
        u1, u2    = st.columns([3, 1], gap="small")
        with u1:
            st.markdown(
                f'<div style="font-family:\'DM Mono\',monospace;font-size:0.75rem;'
                f'color:#6b7280;">👤 {user_name}</div>',
                unsafe_allow_html=True,
            )
        with u2:
            if st.button("🚪", help="Logout", key="logout_btn"):
                logout_user()
                st.rerun()

        st.markdown("---")

        # ── New Research ───────────────────────────────────────────────────
        if st.button("✏️ New Research", use_container_width=True, type="primary", key="new_research_btn"):
            st.session_state["result"]        = None
            st.session_state["active_thread"] = None
            st.session_state["last_topic"]    = ""
            st.session_state["chat_messages"] = []
            st.session_state["followups"]     = []
            st.session_state["active_mode"]   = "research"
            st.rerun()

        # ── Mode switcher ──────────────────────────────────────────────────
        m1, m2 = st.columns(2, gap="small")
        with m1:
            if st.button(
                "🔍 Research",
                use_container_width=True,
                type="primary" if st.session_state.active_mode == "research" else "secondary",
                key="sidebar_research",
            ):
                st.session_state.active_mode = "research"
                st.rerun()
        with m2:
            if st.button(
                "📄 PDF Chat",
                use_container_width=True,
                type="primary" if st.session_state.active_mode == "rag" else "secondary",
                key="sidebar_rag",
            ):
                st.session_state.active_mode = "rag"
                st.rerun()

        st.markdown("---")

        # ── Model selector ─────────────────────────────────────────────────
        st.markdown("**🤖 Model**")
        selected_model = st.selectbox(
            label="model",
            options=list(MODELS.keys()),
            index=list(MODELS.keys()).index(
                st.session_state.get("selected_model_label", DEFAULT_MODEL)
            ),
            label_visibility="collapsed",
            key="selected_model_name",
        )
        model_info = MODELS[selected_model]
        st.session_state["selected_model_id"]    = model_info["id"]
        st.session_state["selected_model_label"] = selected_model
        st.markdown(f"""
        <div style="background:#1d2125;border:1px solid #2b3036;border-radius:8px;
                    padding:0.5rem 0.9rem;margin-bottom:0.5rem;">
            <span style="font-family:'DM Mono',monospace;font-size:0.65rem;
                    color:#18a689;">● {model_info['badge']}</span>
            <span style="font-size:0.7rem;color:#6b7280;margin-left:0.5rem;">
                {model_info['use_case']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Pipeline agents ────────────────────────────────────────────────
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

        # ── Thread history ─────────────────────────────────────────────────
        threads = st.session_state.get("threads", [])
        active  = st.session_state.get("active_thread")

        if threads:
            st.markdown("**🗂 Research History**")
            groups = _group_threads(threads)
            for group_name, group_threads in groups.items():
                if not group_threads:
                    continue
                st.markdown(
                    f'<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;'
                    f'color:#4b5563;letter-spacing:0.1em;text-transform:uppercase;'
                    f'margin:0.8rem 0 0.3rem;">{group_name}</div>',
                    unsafe_allow_html=True,
                )
                for thread in group_threads:
                    tid   = thread["id"]
                    title = thread.get("title") or thread.get("topic", "Untitled")
                    title = title[:35] + "…" if len(title) > 35 else title
                    is_active = (active == tid)

                    t_col, d_col = st.columns([5, 1], gap="small")
                    with t_col:
                        if st.button(
                            f"{'▶ ' if is_active else ''}{title}",
                            key=f"thread_{tid}",
                            use_container_width=True,
                            type="primary" if is_active else "secondary",
                        ):
                            st.session_state["active_thread"] = tid
                            st.session_state["result"] = {
                                "report":          thread.get("report", ""),
                                "search_results":  thread.get("search_results", ""),
                                "scraped_content": "",
                                "feedback":        thread.get("feedback", ""),
                            }
                            st.session_state["last_topic"]    = thread.get("topic", "")
                            st.session_state["chat_messages"] = []
                            st.session_state["followups"]     = []
                            st.session_state["active_mode"]   = "research"
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
                '<div style="color:#4b5563;font-size:0.82rem;text-align:center;'
                'padding:1rem 0;">No research yet.<br>Run your first search!</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ── Footer ────────────────────────────────────────────────────────
        st.markdown(
            '<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:#6b7280;">'
            'Multi-Agent Research System<br>v1.0 · LangGraph + Supabase'
            '</div>',
            unsafe_allow_html=True,
        )