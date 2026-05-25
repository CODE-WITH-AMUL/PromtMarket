from .base import *  # noqa: F403, F401
import os

# Production security settings — intentionally set here (not from .env)
# These are flags, not secrets. Keep secret values (SECRET_KEY, DB creds)
# in the environment provided by the host.
DEBUG = False

if not ALLOWED_HOSTS:
	raise RuntimeError("ALLOWED_HOSTS must be set for production settings")

# Ensure Django knows it's behind a proxy/load-balancer
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Force HTTPS and secure cookies
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

SECURE_REDIRECT_EXEMPT = []

# Sanity check: fail fast if DEBUG is enabled in production environment
if os.environ.get("DJANGO_ENV", "").lower() == "production" and DEBUG:
	raise RuntimeError("DEBUG must be False in production settings")
