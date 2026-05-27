import streamlit as st
from components.model_selector import get_llm


# ── LLM helper ────────────────────────────────────────────────────────────────
def call_llm(prompt: str) -> str:
    try:
        llm    = get_llm(temperature=0.4)
        result = llm.invoke(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# ── PDF extractor ─────────────────────────────────────────────────────────────
def extract_pdf_text(uploaded_file) -> str:
    import io
    file_bytes = uploaded_file.read()

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = "\n\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages  = [reader.pages[i].extract_text() or "" for i in range(len(reader.pages))]
        text   = "\n\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

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


# ── Entry point ───────────────────────────────────────────────────────────────
def render_pdf_mode():

    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">📄 PDF Intelligence</div>
        <h1>Chat with any<br><em>PDF.</em></h1>
        <p class="hero-sub">
            Upload any PDF — research paper, report, contract, or book —
            and ask questions about it in plain English.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Model badge
    model_label = st.session_state.get("selected_model_label", "⚡ Balanced — Mistral 7B")
    st.markdown(f"""
        <div class="model-badge">
            <div class="model-badge-dot"></div>
            {model_label}
        </div>
    """, unsafe_allow_html=True)

    # File uploader
    uploaded = st.file_uploader(
        label="Upload a PDF", type=["pdf"],
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
        word_count = len(st.session_state.rag_pdf_text.split())
        st.markdown(f"""
        <div class="pdf-bar">
            <div class="pdf-icon-wrap">📄</div>
            <div style="flex:1;min-width:0;">
                <div class="pdf-bar-name">{st.session_state.rag_pdf_name}</div>
                <div class="pdf-bar-meta">{word_count:,} words · ready to chat</div>
            </div>
            <div class="pdf-bar-badge">● LOADED</div>
        </div>
        """, unsafe_allow_html=True)

        # Starter questions
        st.markdown("""
        <div class="section-header">
            <div class="section-title">💡 Quick Questions</div>
            <div class="section-sub">Click to ask instantly</div>
        </div>
        """, unsafe_allow_html=True)

        starters = [
            ("📝", "Summarise this document in 5 bullet points"),
            ("🔍", "What are the key findings?"),
            ("✅", "What conclusions does this document reach?"),
        ]
        s_cols = st.columns(3, gap="small")
        for i, (icon, q) in enumerate(starters):
            with s_cols[i]:
                if st.button(f"{icon}  {q}", key=f"rag_starter_{i}", use_container_width=True):
                    st.session_state.rag_messages.append({"role": "user", "content": q})
                    ctx = st.session_state.rag_pdf_text[:4000]
                    with st.spinner("Thinking…"):
                        ans = call_llm(
                            f"You are a helpful assistant. Answer based ONLY on the document below.\n\n"
                            f"DOCUMENT:\n{ctx}\n\nQuestion: {q}\n\nAnswer clearly."
                        )
                    st.session_state.rag_messages.append({"role": "ai", "content": ans})
                    st.rerun()

        st.markdown("---")

        # Chat section header
        st.markdown("""
        <div class="section-header">
            <div class="section-title">💬 Chat with your PDF</div>
            <div class="section-sub">Ask anything about the document</div>
        </div>
        """, unsafe_allow_html=True)

        # Chat history
        if st.session_state.rag_messages:
            msgs_html = ""
            for msg in st.session_state.rag_messages:
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

        # Input row
        rag_col, send_col = st.columns([6, 1], gap="small")
        with rag_col:
            rag_q = st.text_input(
                label="rag_chat",
                placeholder="e.g. What methodology was used? / List all recommendations…",
                label_visibility="collapsed",
                key="rag_input",
            )
        with send_col:
            rag_send_btn = st.button("Send", use_container_width=True,
                                     type="primary", key="rag_send")

        if rag_send_btn and rag_q.strip():
            st.session_state.rag_messages.append({"role": "user", "content": rag_q.strip()})
            doc_ctx     = st.session_state.rag_pdf_text[:4000]
            history_ctx = "\n".join(
                [f"{m['role'].upper()}: {m['content']}"
                 for m in st.session_state.rag_messages[-6:]]
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
        act1, act2 = st.columns([1, 1], gap="small")
        with act1:
            if st.session_state.rag_messages:
                if st.button("🗑  Clear Chat", key="rag_clear", use_container_width=True):
                    st.session_state.rag_messages = []
                    st.rerun()
        with act2:
            if st.button("📂  Load New PDF", key="rag_new", use_container_width=True):
                st.session_state.rag_pdf_text = ""
                st.session_state.rag_pdf_name = ""
                st.session_state.rag_messages = []
                st.rerun()

    else:
        # Empty state
        st.markdown("""
        <div class="pdf-dropzone">
            <div class="pdf-dropzone-icon">📄</div>
            <div class="pdf-dropzone-title">Drop your PDF above</div>
            <div class="pdf-dropzone-sub">
                Research papers, contracts, books, reports — upload any PDF
                and start asking questions instantly.
            </div>
        </div>
        """, unsafe_allow_html=True)