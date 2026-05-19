from .base import *  # noqa: F403, F401

if env("DJANGO_ENV", default="development").lower() == "production":
    from .production import *  # noqa: F403, F401
else:
    from .development import *  # noqa: F403, F401
