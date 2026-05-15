try:
    from auth.supabase_client import init_supabase
    from auth.auth_logic import register_user, login_user, logout_user, get_current_user

    __all__ = [
        "init_supabase",
        "register_user",
        "login_user",
        "logout_user",
        "get_current_user",
    ]
except Exception as e:
    print(f"Auth module import warning: {e}")