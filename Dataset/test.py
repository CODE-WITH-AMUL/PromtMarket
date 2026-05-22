import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Promt.settings.base")
django.setup()

from django.conf import settings
from django.db import connection

try:
    connection.ensure_connection()
    print("✅ Database connected")
except Exception as e:
    print("❌ Database error:", e)