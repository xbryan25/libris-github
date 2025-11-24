import os
from dotenv import load_dotenv

from app.utils import get_cookie_max_age, get_refresh_cookie_max_age

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

    XENDIT_SECRET_KEY = os.getenv("XENDIT_SECRET_KEY")
    XENDIT_WEBHOOK_SECRET_KEY = os.getenv("XENDIT_WEBHOOK_SECRET_KEY")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
    JWT_COOKIE_SECURE = False
    JWT_SESSION_COOKIE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_CSRF_PROTECT = (
        os.getenv("JWT_COOKIE_CSRF_PROTECT", "False").lower() == "true"
    )

    # in minutes
    COOKIE_MAX_AGE = get_cookie_max_age()

    # in days
    REFRESH_COOKIE_MAX_AGE = get_refresh_cookie_max_age()
