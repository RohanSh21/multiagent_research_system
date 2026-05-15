import os
from dotenv import load_dotenv
from supabase import create_client, Client

# ── Load .env file explicitly ────────────────────────────────────────────────────
load_dotenv()


def init_supabase() -> Client:
    """Initialize and return Supabase client."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    return create_client(supabase_url, supabase_key)