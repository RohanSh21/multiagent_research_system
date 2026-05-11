import streamlit as st


def render_sidebar() -> None:
    """Renders the full sidebar — brand, mode switcher, agent list, history."""

    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🧠 ResearchMind</div>', unsafe_allow_html=True)

        # ── Mode switcher ──────────────────────────────────────────────────
        st.markdown("**Mode**")
        mode_col1, mode_col2 = st.columns(2, gap="small")
        with mode_col1:
            if st.button(
                "🔍 Research",
                use_container_width=True,
                type="primary" if st.session_state.active_mode == "research" else "secondary",
                key="sidebar_research",
            ):
                st.session_state.active_mode = "research"
                st.rerun()
        with mode_col2:
            if st.button(
                "📄 PDF Chat",
                use_container_width=True,
                type="primary" if st.session_state.active_mode == "rag" else "secondary",
                key="sidebar_rag",
            ):
                st.session_state.active_mode = "rag"
                st.rerun()

        st.markdown("---")

        # ── Pipeline agents list ───────────────────────────────────────────
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

        # ── Recent searches history ────────────────────────────────────────
        if st.session_state.history:
            st.markdown("**Recent Searches**")
            for h in reversed(st.session_state.history[-6:]):
                st.markdown(
                    f'<div class="history-item">📌 {h}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── Footer ────────────────────────────────────────────────────────
        st.markdown(
            '<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:#6b7280;">'
            'Multi-Agent Research System<br>v1.0 · LangGraph + LangChain'
            '</div>',
            unsafe_allow_html=True,
        )