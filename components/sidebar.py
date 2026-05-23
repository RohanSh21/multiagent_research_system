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
        if diff == 0:     groups["Today"].append(t)
        elif diff == 1:   groups["Yesterday"].append(t)
        elif diff <= 7:   groups["Last 7 Days"].append(t)
        else:             groups["Older"].append(t)
    return groups


def render_sidebar() -> None:
    with st.sidebar:

        # ── Brand ─────────────────────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-brand">🧠 ResearchMind</div>',
            unsafe_allow_html=True,
        )

        # ── User info + logout ─────────────────────────────────────────────
        is_guest  = st.session_state.get("is_guest", False)
        user      = st.session_state.get("user", {})
        user_name = "Guest" if is_guest else user.get("full_name", "User")

        u1, u2 = st.columns([3, 1], gap="small")
        with u1:
            st.markdown(
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;'
                f'color:#555;padding:0.3rem 0;">👤 {user_name}</div>',
                unsafe_allow_html=True,
            )
        with u2:
            if st.button("↩", help="Logout", key="logout_btn"):
                logout_user()
                st.session_state["is_guest"] = False
                st.rerun()

        # Guest banner
        if is_guest:
            st.markdown("""
            <div class="guest-banner">
                ⚡ Guest mode — sign in to save history
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ── New Research ───────────────────────────────────────────────────
        if st.button("＋ New Research", use_container_width=True,
                     type="primary", key="new_research_btn"):
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
                "🔍 Research", use_container_width=True,
                type="primary" if st.session_state.active_mode == "research" else "secondary",
                key="sidebar_research",
            ):
                st.session_state.active_mode = "research"
                st.rerun()
        with m2:
            if st.button(
                "📄 PDF Chat", use_container_width=True,
                type="primary" if st.session_state.active_mode == "rag" else "secondary",
                key="sidebar_rag",
            ):
                st.session_state.active_mode = "rag"
                st.rerun()

        st.markdown("---")

        # ── Model selector ─────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.68rem;font-weight:600;color:#555;'
            'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.4rem;">'
            'Model</div>',
            unsafe_allow_html=True,
        )
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
        <div style="background:#111;border:1px solid #222;border-radius:8px;
                    padding:6px 10px;margin-top:4px;margin-bottom:4px;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                         color:#10b981;">● {model_info['badge']}</span>
            <span style="font-size:0.72rem;color:#555;margin-left:6px;">
                {model_info['use_case']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Pipeline agents ────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.68rem;font-weight:600;color:#555;'
            'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.5rem;">'
            'Agents</div>',
            unsafe_allow_html=True,
        )
        for icon, name, desc in [
            ("🔍", "Search", "Tavily web search"),
            ("📄", "Reader", "Firecrawl scraper"),
            ("✍️", "Writer", "Mistral LLM"),
            ("🔬", "Critic", "Quality reviewer"),
        ]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;
                        padding:5px 4px;margin-bottom:2px;">
                <span style="font-size:0.9rem;">{icon}</span>
                <div>
                    <div style="font-size:0.78rem;font-weight:500;
                                color:#888;line-height:1.2;">{name}</div>
                    <div style="font-family:'JetBrains Mono',monospace;
                                font-size:0.6rem;color:#444;">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # ── Thread history ─────────────────────────────────────────────────
        threads = st.session_state.get("threads", [])
        active  = st.session_state.get("active_thread")

        if is_guest:
            st.markdown(
                '<div style="font-size:0.78rem;color:#444;text-align:center;'
                'padding:0.75rem 0;">Sign in to save & view history</div>',
                unsafe_allow_html=True,
            )
        elif threads:
            st.markdown(
                '<div style="font-size:0.68rem;font-weight:600;color:#555;'
                'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.4rem;">'
                'History</div>',
                unsafe_allow_html=True,
            )
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
                    title     = title[:32] + "…" if len(title) > 32 else title
                    is_active = (active == tid)

                    t_col, d_col = st.columns([5, 1], gap="small")
                    with t_col:
                        if st.button(
                            title, key=f"thread_{tid}",
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
                '<div style="font-size:0.78rem;color:#444;text-align:center;'
                'padding:0.75rem 0;">No history yet</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ── Footer ────────────────────────────────────────────────────────
        st.markdown(
            '<div style="font-family:\'JetBrains Mono\',monospace;'
            'font-size:0.62rem;color:#333;">'
            'v1.0 · LangGraph + Supabase</div>',
            unsafe_allow_html=True,
        )