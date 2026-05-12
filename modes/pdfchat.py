import streamlit as st
from components.model_selector import get_llm


# ── LLM helper ─────────────────────────────────────────────────────────────────
def call_llm(prompt: str) -> str:
    try:
        llm    = get_llm(temperature=0.4)
        result = llm.invoke(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# ── PDF text extractor ──────────────────────────────────────────────────────────
def extract_pdf_text(uploaded_file) -> str:
    """Extract plain text from an uploaded PDF — tries multiple libraries."""
    import io
    file_bytes = uploaded_file.read()

    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = "\n\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    # Try PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages  = [reader.pages[i].extract_text() or "" for i in range(len(reader.pages))]
        text   = "\n\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    # Try pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages  = [page.extract_text() or "" for page in reader.pages]
        text   = "\n\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    return "ERROR_READING_PDF: No PDF library found. Run: pip install pdfplumber"


# ── Main PDF chat mode renderer ─────────────────────────────────────────────────
def render_pdf_mode():
    """Main entry point — renders the full PDF chat mode UI."""

    # Hero
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

    # Model indicator
    model_label = st.session_state.get("selected_model_label", "⚡ Balanced — Mistral 7B")
    st.markdown(
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.72rem;'
        f'color:#6b7280;margin-bottom:1rem;">🤖 Using: {model_label}</div>',
        unsafe_allow_html=True,
    )

    # Upload zone
    uploaded = st.file_uploader(
        label="Upload a PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help="Max ~50 pages works best",
    )

    if uploaded:
        if uploaded.name != st.session_state.rag_pdf_name:
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
        <div class="pdf-bar">
            <span style="font-size:1.4rem;">📄</span>
            <div>
                <div class="pdf-bar-name">{st.session_state.rag_pdf_name}</div>
                <div class="pdf-bar-meta">{len(st.session_state.rag_pdf_text.split()):,} words · ready to chat</div>
            </div>
            <div class="pdf-bar-badge">● LOADED</div>
        </div>
        """, unsafe_allow_html=True)

        # Quick starter questions
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

        # Chat input
        rag_col, rag_send = st.columns([6, 1], gap="small")
        with rag_col:
            rag_q = st.text_input(
                label="rag_chat",
                placeholder="e.g. What methodology was used? / List all recommendations?",
                label_visibility="collapsed",
                key="rag_input",
            )
        with rag_send:
            rag_send_btn = st.button("Send ➤", use_container_width=True, key="rag_send")

        if rag_send_btn and rag_q.strip():
            st.session_state.rag_messages.append({"role": "user", "content": rag_q.strip()})
            doc_ctx     = st.session_state.rag_pdf_text[:4000]
            history_ctx = "\n".join(
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

        # Action buttons
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
        # No PDF uploaded yet — placeholder
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