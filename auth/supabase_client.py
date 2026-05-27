import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


def init_supabase() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
    return create_client(supabase_url, supabase_key)


def get_google_oauth_url() -> str:
    """
    Generate Google OAuth URL using PKCE flow.
    Redirects back to the app with ?code=... after Google auth.
    """
    try:
        supabase = init_supabase()
        app_url  = os.getenv("APP_URL", "http://localhost:8501")

        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to":     app_url,
                "scopes":          "email profile",
                "query_params": {
                    "access_type": "offline",
                    "prompt":      "consent",
                },
            }
        })
        return response.url if hasattr(response, "url") else None
    except Exception as e:
        print(f"OAuth URL error: {e}")
        return None


def get_user_from_code(code: str) -> dict:
    """Exchange auth code for user — PKCE flow."""
    try:
        supabase = init_supabase()
        response = supabase.auth.exchange_code_for_session({"auth_code": code})

        if response and hasattr(response, "user") and response.user:
            user      = response.user
            email     = user.email
            full_name = (
                user.user_metadata.get("full_name")
                or user.user_metadata.get("name")
                or email.split("@")[0]
            )
            user_id = str(user.id)

            # Upsert user into users table
            try:
                existing = init_supabase().table("users").select("id").eq("email", email).execute()
                if not existing.data:
                    init_supabase().table("users").insert({
                        "id":            user_id,
                        "email":         email,
                        "full_name":     full_name,
                        "password_hash": "oauth_google",
                    }).execute()
            except Exception:
                pass

            return {"id": user_id, "email": email, "full_name": full_name}

    except Exception as e:
        print(f"Code exchange error: {e}")
    return None


def get_threads_for_user(user_id: str) -> list:
    """Load research history for a user."""
    try:
        supabase = init_supabase()
        response = supabase.table("research_history").select(
            "id, topic, title, report, search_results, feedback, created_at"
        ).eq("user_id", user_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception:
        return []