import streamlit as st
from auth.auth_logic import login_user, register_user


def render_auth_page():
    """Renders login/signup page when user is not authenticated."""

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="text-align:center;padding:2rem 0;">
            <div style="font-size:2.5rem;margin-bottom:0.5rem;">🧠</div>
            <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                        background:linear-gradient(135deg,#fff 30%,#4fffb0 70%);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;margin-bottom:0.5rem;">
                ResearchMind AI
            </div>
            <div style="color:#6b7280;font-size:0.95rem;margin-bottom:2rem;">
                Deep research powered by AI agents
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Tab switcher ───────────────────────────────────────────────────
        auth_mode = st.radio(
            label="auth_mode",
            options=["Login", "Sign Up"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_tab",
        )

        st.markdown("")

        if auth_mode == "Login":
            render_login()
        else:
            render_signup()


def render_login():
    """Login form."""
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                color:#e8eaf0;margin-bottom:1.5rem;">
        Welcome Back
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

    login_btn = st.button("🔓 Login", use_container_width=True, type="primary")

    if login_btn:
        if not email or not password:
            st.error("Please fill in all fields")
        else:
            with st.spinner("Logging in…"):
                result = login_user(email, password)

            if result["success"]:
                # ── Store user + threads in session state ──────────────────
                st.session_state["authenticated"] = True
                st.session_state["user"]          = result["user"]
                st.session_state["threads"]       = result.get("threads", [])
                st.session_state["active_thread"] = None
                st.session_state["result"]        = None
                st.session_state["chat_messages"] = []
                st.session_state["history"]       = [
                    t.get("topic", "") for t in result.get("threads", [])
                ]
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])


def render_signup():
    """Signup form."""
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
                color:#e8eaf0;margin-bottom:1.5rem;">
        Create Account
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
        placeholder="••••••••",
        type="password",
        key="signup_password",
    )

    password_confirm = st.text_input(
        label="Confirm Password",
        placeholder="••••••••",
        type="password",
        key="signup_confirm",
    )

    signup_btn = st.button("✨ Sign Up", use_container_width=True, type="primary")

    if signup_btn:
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
                st.info("✅ Account created! Switch to Login tab to sign in.")
            else:
                st.error(result["message"])