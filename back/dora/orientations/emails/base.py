from django.conf import settings
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.utils import timezone
from mjml import mjml2html

from dora.core.emails import send_mail
from dora.orientations.models import ContactPreference

debug = settings.ORIENTATION_EMAILS_DEBUG


class OrientationEmailBackend:
    # Par défaut, on cherche les templates à la racine (celles de Dora).
    # Celles des emplois sont sur "emplois/"
    template_dir = ""

    # Étiquette insérée dans le sujet des mails de test
    role_label = ""

    def _debug(self):
        return debug

    def _subject(self, orientation_stage, recipient, base):
        if self._debug():
            return f"[{orientation_stage} - {self.role_label}{recipient}] {base}"
        return base

    def _template(self, name):
        return f"{self.template_dir}{name}"

    def _has_distinct_referent(self, orientation):
        return (
            orientation.referent_email
            and orientation.referent_email != orientation.prescriber_info.email
        )

    def _beneficiaries_has_alternate_contact_methods(self, orientation):
        beneficiaries_contact_methods = [
            method
            for method in [
                orientation.beneficiary_phone,
                orientation.beneficiary_email,
                orientation.beneficiary_other_contact_method,
            ]
            if method
        ]

        return len(beneficiaries_contact_methods) > len(
            orientation.beneficiary_contact_preferences
        )

    def _send(
        self,
        *,
        subject,
        to,
        template,
        context,
        from_email=None,
        reply_to=None,
        cc=None,
    ):
        kwargs = {"tags": ["orientation"]}
        if from_email is not None:
            kwargs["from_email"] = from_email
        if reply_to is not None:
            kwargs["reply_to"] = reply_to
        if cc is not None:
            kwargs["cc"] = cc
        send_mail(
            subject,
            to,
            mjml2html(render_to_string(self._template(template), context)),
            **kwargs,
        )

    def _orientation_reminder_ctx(self, orientation):
        return {
            "data": orientation,
            "support_email": settings.SUPPORT_EMAIL,
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
            "elapsed_days": (timezone.now() - orientation.creation_date).days,
            "ContactPreference": ContactPreference,
            "beneficiaries_has_alternate_contact_methods": self._beneficiaries_has_alternate_contact_methods(
                orientation
            ),
            "attachments": [
                {"name": a, "url": default_storage.url(a)}
                for a in orientation.beneficiary_attachments
            ],
        }

    def send_reminder(self, orientation, context=None):
        # Le mail de relance est le même pour Dora et Les emplois
        context = context or self._orientation_reminder_ctx(orientation)
        send_mail(
            self._subject(
                "Notification",
                "Structure",
                "Relance – Demande d’orientation en attente",
            ),
            orientation.get_contact_email(),
            mjml2html(render_to_string("notification-structure.mjml", context)),
            tags=["orientation"],
        )

    def send_created(self, orientation):
        raise NotImplementedError

    def send_accepted(self, orientation, prescriber_message, beneficiary_message):
        raise NotImplementedError

    def send_rejected(self, orientation, message):
        raise NotImplementedError

    def send_expired(self, orientation, start_date):
        raise NotImplementedError

    def send_message_to_prescriber(self, orientation, message, cc):
        raise NotImplementedError

    def send_message_to_beneficiary(self, orientation, message, cc):
        raise NotImplementedError
