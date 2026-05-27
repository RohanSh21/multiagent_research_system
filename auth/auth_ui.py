import streamlit as st
from auth.auth_logic import login_user, register_user
from auth.supabase_client import get_google_oauth_url, handle_oauth_callback


def _check_oauth_callback():
    try:
        params        = st.query_params
        access_token  = params.get("access_token")
        refresh_token = params.get("refresh_token")
        if access_token and refresh_token:
            from auth.supabase_client import init_supabase
            user = handle_oauth_callback(access_token, refresh_token)
            if user:
                supabase = init_supabase()
                history  = supabase.table("research_history").select(
                    "id, topic, title, report, search_results, feedback, created_at"
                ).eq("user_id", user["id"]).order("created_at", desc=True).execute()
                threads  = history.data if history.data else []
                st.session_state.update({
                    "authenticated": True, "user": user,
                    "is_guest": False, "threads": threads,
                    "active_thread": None, "result": None,
                    "chat_messages": [],
                    "history": [t.get("topic", "") for t in threads],
                })
                st.query_params.clear()
                st.rerun()
    except Exception:
        pass


def render_auth_page():
    _check_oauth_callback()

    # Centre column
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("<div style='padding:3rem 0 1rem;'>", unsafe_allow_html=True)

        # ── Logo ──────────────────────────────────────────────────────
        st.markdown("""
        <div class="auth-logo">
            <div style="display:flex;justify-content:center;margin-bottom:0.75rem;">
                <svg width="48" height="48" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
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
            </div>
            <div style="font-size:1.6rem;font-weight:800;letter-spacing:-0.04em;background:linear-gradient(135deg,#93c5fd,#60a5fa,#2f6feb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Nexus AI</div>
            <div class="auth-logo-sub">Deep research powered by AI agents</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Google OAuth ───────────────────────────────────────────────
        google_url = get_google_oauth_url()
        if google_url:
            st.markdown(f"""
            <a href="{google_url}" target="_self" style="text-decoration:none;display:block;margin-bottom:1rem;">
                <div style="
                    display:flex;align-items:center;justify-content:center;gap:12px;
                    background:#fff;color:#1f1f1f;border:1px solid #dadce0;
                    border-radius:12px;padding:0.75rem 1rem;
                    font-family:'Inter',sans-serif;font-size:0.92rem;font-weight:500;
                    cursor:pointer;transition:box-shadow 0.15s;
                    box-sizing:border-box;width:100%;
                ">
                    <svg width="18" height="18" viewBox="0 0 48 48">
                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                    </svg>
                    Continue with Google
                </div>
            </a>
            """, unsafe_allow_html=True)
        else:
            st.warning("Google Sign-In unavailable. Use email/password below.")

        st.markdown('<div class="auth-divider">or continue with email</div>', unsafe_allow_html=True)

        # ── Login / Sign Up tabs ───────────────────────────────────────
        auth_mode = st.radio(
            label="auth_mode", options=["Login", "Sign Up"],
            horizontal=True, label_visibility="collapsed", key="auth_tab",
        )
        st.markdown("")

        if auth_mode == "Login":
            _render_login()
        else:
            _render_signup()

        # ── Guest ──────────────────────────────────────────────────────
        st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)

        if st.button("👤  Continue as Guest", use_container_width=True, key="guest_btn"):
            st.session_state.update({
                "authenticated": True, "user": None,
                "is_guest": True, "threads": [],
                "active_thread": None, "result": None,
                "chat_messages": [], "history": [],
            })
            st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:0.5rem;font-size:0.72rem;color:var(--text3);">
            Guest mode — research history won't be saved
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


def _render_login():
    st.markdown('<div class="auth-form-title">Welcome back</div>', unsafe_allow_html=True)
    email    = st.text_input("Email", placeholder="you@example.com", key="login_email")
    password = st.text_input("Password", placeholder="••••••••", type="password", key="login_password")

    if st.button("Sign in →", use_container_width=True, type="primary", key="login_btn"):
        if not email or not password:
            st.error("Please fill in all fields.")
        else:
            with st.spinner("Signing in…"):
                result = login_user(email, password)
            if result["success"]:
                st.session_state.update({
                    "authenticated": True, "user": result["user"],
                    "is_guest": False, "threads": result.get("threads", []),
                    "active_thread": None, "result": None, "chat_messages": [],
                    "history": [t.get("topic", "") for t in result.get("threads", [])],
                })
                st.rerun()
            else:
                st.error(result["message"])


def _render_signup():
    st.markdown('<div class="auth-form-title">Create account</div>', unsafe_allow_html=True)
    full_name        = st.text_input("Full Name", placeholder="John Doe", key="signup_name")
    email            = st.text_input("Email", placeholder="you@example.com", key="signup_email")
    password         = st.text_input("Password", placeholder="Min. 6 characters", type="password", key="signup_password")
    password_confirm = st.text_input("Confirm Password", placeholder="••••••••", type="password", key="signup_confirm")

    if st.button("Create account →", use_container_width=True, type="primary", key="signup_btn"):
        if not email or not password or not full_name:
            st.error("Please fill in all fields.")
        elif password != password_confirm:
            st.error("Passwords don't match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            with st.spinner("Creating account…"):
                result = register_user(email, password, full_name)
            if result["success"]:
                st.success(result["message"])
                st.info("✅ Switch to the Login tab to sign in.")
            else:
                st.error(result["message"])