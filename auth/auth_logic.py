import streamlit as st
import hashlib
import os
from auth.supabase_client import init_supabase


def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email: str, password: str, full_name: str = "") -> dict:
    """Register a new user in Supabase."""
    try:
        supabase = init_supabase()

        # Check if user already exists
        response = supabase.table("users").select("id").eq("email", email).execute()
        if response.data:
            return {"success": False, "message": "Email already registered"}

        hashed_pwd = hash_password(password)

        response = supabase.table("users").insert({
            "email":         email,
            "password_hash": hashed_pwd,
            "full_name":     full_name or email.split("@")[0],
        }).execute()

        if response.data:
            return {"success": True, "message": "Registration successful! Please login."}
        else:
            return {"success": False, "message": "Registration failed"}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def login_user(email: str, password: str) -> dict:
    """Login user and load their research history."""
    try:
        supabase = init_supabase()

        response = supabase.table("users").select(
            "id, email, full_name, password_hash"
        ).eq("email", email).execute()

        if not response.data:
            return {"success": False, "user": None, "message": "Email not found"}

        user = response.data[0]
        hashed_pwd = hash_password(password)

        if user["password_hash"] != hashed_pwd:
            return {"success": False, "user": None, "message": "Incorrect password"}

        # Load research history from Supabase
        history_response = supabase.table("research_history").select(
            "id, topic, title, report, search_results, feedback, created_at"
        ).eq("user_id", user["id"]).order("created_at", desc=True).execute()

        threads = history_response.data if history_response.data else []

        return {
            "success": True,
            "user": {
                "id":        user["id"],
                "email":     user["email"],
                "full_name": user["full_name"],
            },
            "threads": threads,
            "message": "Login successful!",
        }

    except Exception as e:
        return {"success": False, "user": None, "message": f"Error: {str(e)}"}


def save_research(user_id: str, topic: str, report: str,
                  search_results: str = "", feedback: str = "") -> bool:
    """Save a research result to Supabase."""
    try:
        supabase = init_supabase()

        # Title = first 60 chars of topic
        title = topic[:60] if len(topic) > 60 else topic

        supabase.table("research_history").insert({
            "user_id":        user_id,
            "topic":          topic,
            "title":          title,
            "report":         report,
            "search_results": search_results[:5000] if search_results else "",
            "feedback":       feedback[:2000]        if feedback else "",
        }).execute()

        return True

    except Exception as e:
        print(f"Error saving research: {e}")
        return False


def delete_thread(thread_id: str) -> bool:
    """Delete a research thread from Supabase."""
    try:
        supabase = init_supabase()
        supabase.table("research_history").delete().eq("id", thread_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting thread: {e}")
        return False


def get_current_user() -> dict:
    """Get current logged-in user from session state."""
    return st.session_state.get("user", None)


def logout_user():
    """Logout current user and clear session."""
    st.session_state["user"]          = None
    st.session_state["authenticated"] = False
    st.session_state["threads"]       = []
    st.session_state["active_thread"] = None
    st.session_state["result"]        = None
    st.session_state["history"]       = []
    st.session_state["chat_messages"] = []