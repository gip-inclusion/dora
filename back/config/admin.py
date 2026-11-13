import enum
import logging

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.crypto import salted_hmac
from django_otp.admin import OTPAdminAuthenticationForm, OTPAdminSite

from dora.core.throttling import get_client_ip

logger = logging.getLogger("dora.logs.core")
# Hors `ActionLog` (logs applicatifs uniquement) : un attaquant bloqué ne doit pas
# pouvoir remplir la base
blocked_logger = logging.getLogger("dora.admin")

# la classe d'admin `OTPAdminSite` utilise des variables initialisées dans le middleware :
# elle ne peut faire office d'admin si l'OTP n'est pas activé

admin_class = OTPAdminSite if settings.DJANGO_ADMIN_2FA_ENABLED else AdminSite
login_form_class = (
    OTPAdminAuthenticationForm
    if settings.DJANGO_ADMIN_2FA_ENABLED
    else AdminAuthenticationForm
)


class AdminLoginAction(enum.StrEnum):
    """
    Actions loggées pour la connexion à l'admin.
    """

    SUCCEEDED = "admin_login_succeeded"
    FAILED = "admin_login_failed"


class AdminLoginForm(login_form_class):
    """Formulaire de connexion à l'admin, limité et journalisé.

    Après `ADMIN_LOGIN_MAX_FAILURES_PER_IP` échecs depuis une même IP, ou
    `ADMIN_LOGIN_MAX_FAILURES_PER_EMAIL` pour un même email, les tentatives sont
    refusées pendant `ADMIN_LOGIN_LOCKOUT_MINUTES` après le dernier échec.
    """

    # Étapes normales de la 2FA, ni comptées ni journalisées comme des échecs.
    # Les autres erreurs le sont, y compris celles sans code (django-otp en lève
    # quand il ralentit lui-même les essais sur un appareil).
    OTP_STEP_ERROR_CODES = {
        "token_required",
        "device_required",
        "challenge_message",
        "challenge_exception",
        "not_interactive",
    }

    def clean(self):
        email = (self.cleaned_data.get("username") or "").strip().lower()
        if not email or not self.cleaned_data.get("password"):
            # Champ manquant : aucune authentification n'est tentée
            return super().clean()

        ip = get_client_ip(self.request)
        # Le champ n'est pas validé comme un email : il peut contenir un mot de
        # passe saisi par erreur, qui ne doit apparaître ni en cache ni en log
        email_digest = salted_hmac(
            "admin-login", email, algorithm="sha256"
        ).hexdigest()[:32]
        email_key = f"admin-login:email:{email_digest}"
        limits = {
            f"admin-login:ip:{ip}": settings.ADMIN_LOGIN_MAX_FAILURES_PER_IP,
            email_key: settings.ADMIN_LOGIN_MAX_FAILURES_PER_EMAIL,
        }

        counts = cache.get_many(limits)
        if any(counts.get(key, 0) >= limit for key, limit in limits.items()):
            # Le formateur JSON ne retient ni `args` ni `extra` : l'empreinte va dans
            # le message (l'IP y figure déjà, via `network.client.ip`)
            blocked_logger.warning(
                "Tentative de connexion à l'admin bloquée (email : %s)", email_digest
            )
            raise ValidationError(
                "Trop de tentatives de connexion, réessayez dans "
                f"{settings.ADMIN_LOGIN_LOCKOUT_MINUTES} minutes.",
                code="too_many_attempts",
            )

        try:
            cleaned_data = super().clean()
        except ValidationError as e:
            reasons = [error.code for error in e.error_list]
            if not set(reasons) <= self.OTP_STEP_ERROR_CODES:
                self._record_failure(email, email_digest, ip, limits, reasons)
            raise

        cache.delete(email_key)
        user = self.get_user()
        logger.info(
            "Connexion à l'admin",
            {
                "legal": True,
                "ip": ip,
                "email": user.email,
                "action": AdminLoginAction.SUCCEEDED,
                "userId": user.pk,
            },
        )
        return cleaned_data

    def _record_failure(self, email, email_digest, ip, limits, reasons):
        # Des requêtes parallèles peuvent passer la vérification de la limite
        # avant que leurs échecs soient comptés : le dépassement reste borné par
        # le nombre de workers, et chaque échec est compté et journalisé
        blocked = False
        for key, limit in limits.items():
            blocked |= _increment(key) >= limit

        log_payload = {"legal": True, "ip": ip}
        if get_user_model().objects.filter(email__iexact=email).exists():
            log_payload["email"] = email
        else:
            log_payload["emailDigest"] = email_digest
        logger.warning(
            "Échec de connexion à l'admin",
            log_payload
            | {
                "action": AdminLoginAction.FAILED,
                "reasons": reasons,
                "blocked": blocked,
            },
        )


def _increment(key):
    """Incrémente le compteur de façon atomique et repousse son expiration."""
    timeout = settings.ADMIN_LOGIN_LOCKOUT_MINUTES * 60
    cache.add(key, 0, timeout)
    try:
        count = cache.incr(key)
    except ValueError:
        # La clé a expiré entre `add` et `incr`
        count = 1
        cache.set(key, count, timeout)
    # Le blocage court jusqu'à `timeout` après le dernier échec
    cache.touch(key, timeout)
    return count


class AdminSite(admin_class):
    site_header = "DORA administration"
    site_title = f"DORA admin ({settings.ENVIRONMENT})"
    site_url = settings.FRONTEND_URL
    login_form = AdminLoginForm
