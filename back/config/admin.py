from django.conf import settings
from django.contrib.admin import AdminSite
from django_otp.admin import OTPAdminSite

# la classe d'admin `OTPAdminSite` utilise des variables initialisées dans le middleware :
# elle ne peut faire office d'admin si l'OTP n'est pas activé

admin_class = OTPAdminSite if settings.DJANGO_ADMIN_2FA_ENABLED else AdminSite


class AdminSite(admin_class):
    site_header = "DORA administration"
    site_title = f"DORA admin ({settings.ENVIRONMENT})"
    site_url = settings.FRONTEND_URL
