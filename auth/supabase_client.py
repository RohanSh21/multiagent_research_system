import os
from dotenv import load_dotenv
from supabase import create_client, Client

# ── Load .env ────────────────────────────────────────────────────────────────────
load_dotenv()


def init_supabase() -> Client:
    """Initialize and return Supabase client."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    return create_client(supabase_url, supabase_key)


def get_google_oauth_url() -> str:
    """Generate Google OAuth URL via Supabase."""
    try:
        supabase = init_supabase()

        # Detect environment for redirect
        import streamlit as st
        redirect_url = os.getenv(
            "APP_URL",
            "http://localhost:8501"
        )

        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_url,
            }
        })
        return response.url if hasattr(response, "url") else None

    except Exception as e:
        print(f"OAuth error: {e}")
        return None


def handle_oauth_callback(access_token: str, refresh_token: str) -> dict:
    """
    Handle OAuth callback — set session and get user data.
    Returns user dict or None.
    """
    try:
        supabase = init_supabase()

        # Set the session with tokens
        session = supabase.auth.set_session(access_token, refresh_token)

        if session and session.user:
            user = session.user
            email     = user.email
            full_name = (
                user.user_metadata.get("full_name")
                or user.user_metadata.get("name")
                or email.split("@")[0]
            )
            user_id = str(user.id)

            # Upsert user into our users table
            try:
                existing = supabase.table("users").select("id").eq(
                    "email", email
                ).execute()

                if not existing.data:
                    supabase.table("users").insert({
                        "id":            user_id,
                        "email":         email,
                        "full_name":     full_name,
                        "password_hash": "oauth_user",
                    }).execute()
            except Exception:
                pass

            return {
                "id":        user_id,
                "email":     email,
                "full_name": full_name,
            }

    except Exception as e:
        print(f"OAuth callback error: {e}")

    return None