"""
FILE: libris/app/config.py (COMPLETE - LINTING FIXED)
Replace your entire config.py with this
"""

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

    # Email Configuration - MAILTRAP SETTINGS
    MAIL_SERVER = os.getenv("MAIL_SERVER", "sandbox.smtp.mailtrap.io")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@libris.com")

    print("[CONFIG] Email Configuration Loaded:")
    print(f"  MAIL_SERVER: {MAIL_SERVER}")
    print(f"  MAIL_PORT: {MAIL_PORT}")
    print(f"  MAIL_USE_TLS: {MAIL_USE_TLS}")
    print(f"  MAIL_USE_SSL: {MAIL_USE_SSL}")
