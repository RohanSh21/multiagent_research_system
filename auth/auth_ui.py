import streamlit as st
from auth.auth_logic import login_user, register_user
from auth.supabase_client import get_google_oauth_url, handle_oauth_callback


def _check_oauth_callback():
    """
    Check URL params for OAuth callback tokens.
    Supabase redirects back with access_token and refresh_token in the URL hash.
    Streamlit can read query params from the URL.
    """
    try:
        params = st.query_params
        access_token  = params.get("access_token")
        refresh_token = params.get("refresh_token")

        if access_token and refresh_token:
            from auth.supabase_client import handle_oauth_callback
            from auth.auth_logic import login_user
            from auth.supabase_client import init_supabase

            user = handle_oauth_callback(access_token, refresh_token)
            if user:
                # Load research history
                supabase = init_supabase()
                history_response = supabase.table("research_history").select(
                    "id, topic, title, report, search_results, feedback, created_at"
                ).eq("user_id", user["id"]).order("created_at", desc=True).execute()

                threads = history_response.data if history_response.data else []

                st.session_state["authenticated"] = True
                st.session_state["user"]          = user
                st.session_state["is_guest"]      = False
                st.session_state["threads"]       = threads
                st.session_state["active_thread"] = None
                st.session_state["result"]        = None
                st.session_state["chat_messages"] = []
                st.session_state["history"]       = [
                    t.get("topic", "") for t in threads
                ]

                # Clear query params
                st.query_params.clear()
                st.rerun()
    except Exception as e:
        pass


def render_auth_page():
    """Renders login/signup page with Google OAuth + guest mode."""

    # Check for OAuth callback first
    _check_oauth_callback()

    _, col, _ = st.columns([1, 1.2, 1])

    with col:
        st.markdown("<div style='padding:3rem 0 1rem;'>", unsafe_allow_html=True)

        # Logo
        st.markdown("""
        <div class="auth-logo">
            <div class="auth-logo-icon">🧠</div>
            <div class="auth-logo-title">ResearchMind AI</div>
            <div class="auth-logo-sub">Deep research powered by AI agents</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Google Sign In Button ──────────────────────────────────────────
        google_url = get_google_oauth_url()
        if google_url:
            st.markdown(f"""
            <a href="{google_url}" target="_self" style="text-decoration:none;">
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    background: #ffffff;
                    color: #1f1f1f;
                    border: 1px solid #dadce0;
                    border-radius: 12px;
                    padding: 0.75rem 1rem;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.95rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background 0.15s;
                    margin-bottom: 1rem;
                    width: 100%;
                    box-sizing: border-box;
                ">
                    <svg width="20" height="20" viewBox="0 0 48 48">
                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                        <path fill="none" d="M0 0h48v48H0z"/>
                    </svg>
                    Continue with Google
                </div>
            </a>
            """, unsafe_allow_html=True)
        else:
            st.warning("Google Sign-In unavailable. Please use email/password below.")

        # ── Divider ────────────────────────────────────────────────────────
        st.markdown('<div class="auth-divider">or continue with email</div>',
                    unsafe_allow_html=True)

        # ── Email/Password tabs ────────────────────────────────────────────
        auth_mode = st.radio(
            label="auth_mode",
            options=["Login", "Sign Up"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_tab",
        )

        st.markdown("")

        if auth_mode == "Login":
            _render_login()
        else:
            _render_signup()

        # ── Guest mode ─────────────────────────────────────────────────────
        st.markdown('<div class="auth-divider">or</div>', unsafe_allow_html=True)

        if st.button("👤 Continue as Guest", use_container_width=True, key="guest_btn"):
            st.session_state["authenticated"] = True
            st.session_state["user"]          = None
            st.session_state["is_guest"]      = True
            st.session_state["threads"]       = []
            st.session_state["active_thread"] = None
            st.session_state["result"]        = None
            st.session_state["chat_messages"] = []
            st.session_state["history"]       = []
            st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:0.6rem;font-size:0.75rem;color:#555;">
            Guest mode — history won't be saved
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


def _render_login():
    """Login form."""
    st.markdown("""
    <div style="font-size:1.1rem;font-weight:600;color:#ececec;
                margin-bottom:1.25rem;letter-spacing:-0.02em;">
        Welcome back
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        label="Email",
        placeholder="you@example.com",
        key="login_email",
    )
    password = st.text_input(
        label="Password",
        placeholder="••••••••",
        type="password",
        key="login_password",
    )

    if st.button("Sign in", use_container_width=True, type="primary", key="login_btn"):
        if not email or not password:
            st.error("Please fill in all fields")
        else:
            with st.spinner("Signing in…"):
                result = login_user(email, password)
            if result["success"]:
                st.session_state["authenticated"] = True
                st.session_state["user"]          = result["user"]
                st.session_state["is_guest"]      = False
                st.session_state["threads"]       = result.get("threads", [])
                st.session_state["active_thread"] = None
                st.session_state["result"]        = None
                st.session_state["chat_messages"] = []
                st.session_state["history"]       = [
                    t.get("topic", "") for t in result.get("threads", [])
                ]
                st.rerun()
            else:
                st.error(result["message"])


def _render_signup():
    """Signup form."""
    st.markdown("""
    <div style="font-size:1.1rem;font-weight:600;color:#ececec;
                margin-bottom:1.25rem;letter-spacing:-0.02em;">
        Create account
    </div>
    """, unsafe_allow_html=True)

    full_name = st.text_input(
        label="Full Name",
        placeholder="John Doe",
        key="signup_name",
    )
    email = st.text_input(
        label="Email",
        placeholder="you@example.com",
        key="signup_email",
    )
    password = st.text_input(
        label="Password",
        placeholder="Min. 6 characters",
        type="password",
        key="signup_password",
    )
    password_confirm = st.text_input(
        label="Confirm Password",
        placeholder="••••••••",
        type="password",
        key="signup_confirm",
    )

    if st.button("Create account", use_container_width=True, type="primary", key="signup_btn"):
        if not email or not password or not full_name:
            st.error("Please fill in all fields")
        elif password != password_confirm:
            st.error("Passwords don't match")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters")
        else:
            with st.spinner("Creating account…"):
                result = register_user(email, password, full_name)
            if result["success"]:
                st.success(result["message"])
                st.info("✅ Switch to Login tab to sign in.")
            else:
                st.error(result["message"])