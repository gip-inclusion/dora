from django.conf import settings
from django.contrib import admin


class AdminSite(admin.AdminSite):
    site_header = "DORA administration"
    site_title = f"DORA admin ({settings.ENVIRONMENT})"
    site_url = settings.FRONTEND_URL
