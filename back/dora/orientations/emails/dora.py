from django.conf import settings
from django.core.files.storage import default_storage

from .base import OrientationEmailBackend

debug = settings.ORIENTATION_EMAILS_DEBUG


class DoraBackend(OrientationEmailBackend):
    template_dir = ""
    role_label = ""

    def _debug(self):
        return debug

    def _structure_from_email(self, orientation):
        return (
            f"{orientation.get_structure_name()} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        )

    def _prescriber_full_name_from_email(self, orientation):
        return (
            f"{orientation.prescriber_info.full_name} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        )

    # --- Création ---------------------------------------------------------

    def _orientation_created_ctx(self, orientation):
        from dora.orientations.models import ContactPreference

        return {
            "data": orientation,
            "ContactPreference": ContactPreference,
            "support_email": settings.SUPPORT_EMAIL,
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
            "beneficiaries_has_alternate_contact_methods": self._beneficiaries_has_alternate_contact_methods(
                orientation
            ),
            "service_address": orientation.get_service_address_line(),
            "attachments": [
                {"name": a, "url": default_storage.url(a)}
                for a in orientation.beneficiary_attachments
            ],
        }

    def send_created_to_structure(self, orientation, context=None):
        context = context or self._orientation_created_ctx(orientation)
        self._send(
            subject=self._subject(
                "Envoyée", "Structure porteuse", "Nouvelle demande d’orientation reçue"
            ),
            to=orientation.get_contact_email(),
            template="orientation-created-structure.mjml",
            context=context,
            from_email=self._prescriber_full_name_from_email(orientation),
            reply_to=[orientation.prescriber_info.email],
        )

    def _send_created_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Envoyée", "Prescripteur", "Votre demande a bien été transmise !"
            ),
            to=orientation.prescriber_info.email,
            template="orientation-created-prescriber.mjml",
            context=context,
            reply_to=[orientation.get_contact_email()],
        )

    def _send_created_to_referent(self, orientation, context):
        if not self._has_distinct_referent(orientation):
            return
        self._send(
            subject=self._subject(
                "Envoyée",
                "Conseiller référent",
                "Notification d’une demande d’orientation",
            ),
            to=orientation.referent_email,
            template="orientation-created-referent.mjml",
            context=context,
            reply_to=[orientation.prescriber_info.email],
        )

    def _send_created_to_beneficiary(self, orientation, context):
        if not orientation.beneficiary_email:
            return
        self._send(
            subject=self._subject(
                "Envoyée",
                "Bénéficiaire",
                "Une orientation a été effectuée en votre nom",
            ),
            to=orientation.beneficiary_email,
            template="orientation-created-beneficiary.mjml",
            context=context,
            from_email=self._prescriber_full_name_from_email(orientation),
            reply_to=[orientation.prescriber_info.email],
        )

    def send_created(self, orientation):
        context = self._orientation_created_ctx(orientation)
        self.send_created_to_structure(orientation, context)
        self._send_created_to_prescriber(orientation, context)
        self._send_created_to_referent(orientation, context)
        self._send_created_to_beneficiary(orientation, context)

    # --- Validation --------------------------------------------------------

    def _orientation_accepted_ctx(
        self, orientation, prescriber_message="", beneficiary_message=""
    ):
        placeholder = "#SERVICE_ADDRESS#"
        prescriber_message = prescriber_message.replace(
            placeholder, orientation.get_service_address_line()
        )
        beneficiary_message = beneficiary_message.replace(
            placeholder, orientation.get_service_address_line()
        )

        return {
            "data": orientation,
            "support_email": settings.SUPPORT_EMAIL,
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
            "prescriber_message": prescriber_message,
            "beneficiary_message": beneficiary_message,
        }

    def send_accepted_to_structure(self, orientation, context=None):
        context = context or self._orientation_accepted_ctx(orientation)
        self._send(
            subject=self._subject(
                "Validée", "Structure porteuse", "Vous venez de valider une demande 🎉"
            ),
            to=[orientation.get_contact_email()],
            template="orientation-accepted-structure.mjml",
            context=context,
        )

    def _send_accepted_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Validée", "Prescripteur", "Votre demande a été acceptée ! 🎉"
            ),
            to=orientation.prescriber_info.email,
            template="orientation-accepted-prescriber.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
        )

    def _send_accepted_to_referent(self, orientation, context):
        if not self._has_distinct_referent(orientation):
            return
        self._send(
            subject=self._subject(
                "Validée",
                "Conseiller référent",
                "Notification de l’acceptation d’une demande d’orientation",
            ),
            to=orientation.referent_email,
            template="orientation-accepted-referent.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.prescriber_info.email],
        )

    def _send_accepted_to_beneficiary(self, orientation, context):
        if not orientation.beneficiary_email:
            return
        self._send(
            subject=self._subject(
                "Validée", "Bénéficiaire", "Votre demande a été acceptée ! 🎉"
            ),
            to=orientation.beneficiary_email,
            template="orientation-accepted-beneficiary.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
        )

    def send_accepted(self, orientation, prescriber_message, beneficiary_message):
        context = self._orientation_accepted_ctx(
            orientation, prescriber_message, beneficiary_message
        )
        self.send_accepted_to_structure(orientation, context)
        self._send_accepted_to_prescriber(orientation, context)
        self._send_accepted_to_referent(orientation, context)
        self._send_accepted_to_beneficiary(orientation, context)

    # --- Refus -------------------------------------------------------------

    def _orientation_rejected_ctx(self, orientation, message=""):
        return {
            "data": orientation,
            "support_email": settings.SUPPORT_EMAIL,
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
            "message": message,
        }

    def send_rejected_to_structure(self, orientation, context=None):
        context = context or self._orientation_rejected_ctx(orientation)
        self._send(
            subject=self._subject(
                "Refusée", "Structure porteuse", "Vous venez de refuser une demande"
            ),
            to=[orientation.get_contact_email()],
            template="orientation-rejected-structure.mjml",
            context=context,
        )

    def _send_rejected_to_beneficiary(self, orientation, context):
        if not orientation.beneficiary_email:
            return
        self._send(
            subject=self._subject(
                "Refusée",
                "Bénéficiaire",
                "Votre demande d’orientation a été refusée",
            ),
            to=[orientation.beneficiary_email],
            template="orientation-rejected-beneficiary.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.prescriber_info.email],
        )

    def _send_rejected_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Refusée",
                "Prescripteur",
                "Votre demande d’orientation a été refusée",
            ),
            to=[orientation.prescriber_info.email],
            template="orientation-rejected-prescriber.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
        )

    def _send_rejected_to_referent(self, orientation, context):
        if not self._has_distinct_referent(orientation):
            return
        self._send(
            subject=self._subject(
                "Refusée",
                "Conseiller référent",
                "Votre demande d’orientation a été refusée",
            ),
            to=[orientation.referent_email],
            template="orientation-rejected-prescriber.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
        )

    def send_rejected(self, orientation, message):
        context = self._orientation_rejected_ctx(orientation, message)
        self.send_rejected_to_structure(orientation, context)
        self._send_rejected_to_beneficiary(orientation, context)
        self._send_rejected_to_prescriber(orientation, context)
        self._send_rejected_to_referent(orientation, context)

    # --- Expiration --------------------------------------------------------

    def _orientation_expired_ctx(self, orientation, start_date):
        return {
            "data": orientation,
            "expiration_period_days": settings.ORIENTATION_EXPIRATION_PERIOD_DAYS,
            "search_link": settings.FRONTEND_URL + "/recherche",
            "start_date": start_date.strftime("%-d %B %Y"),
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
            "with_dora_info": True,
            "with_legal_info": True,
        }

    def send_expired_to_structure(self, orientation, context):
        self._send(
            subject="Cette demande d’orientation a expiré",
            to=orientation.get_contact_email(),
            template="orientation-expired-service.mjml",
            context=context,
        )

    def send_expired(self, orientation, start_date) -> None:
        context = self._orientation_expired_ctx(orientation, start_date)
        self.send_expired_to_structure(orientation, context)
        self._send(
            subject="Cette demande d’orientation a été annulée",
            to=orientation.beneficiary_email,
            template="orientation-expired-beneficiary.mjml",
            context=context,
        )
        for email in {orientation.prescriber_info.email, orientation.referent_email}:
            self._send(
                subject="Votre demande d’orientation a expiré",
                to=email,
                template="orientation-expired-prescriber.mjml",
                context=context,
            )

    # --- Messages de contact -----------------------------------------------

    def send_message_to_prescriber(self, orientation, message, cc):
        context = {
            "data": orientation,
            "message": message,
            "support_email": settings.SUPPORT_EMAIL,
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        }
        self._send(
            subject=self._subject(
                "Contact", "Prescripteur", "Vous avez un nouveau message 📩"
            ),
            to=orientation.prescriber_info.email,
            template="contact-prescriber.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
            cc=cc,
        )

    def send_message_to_beneficiary(self, orientation, message, cc):
        context = {
            "data": orientation,
            "message": message,
            "support_email": settings.SUPPORT_EMAIL,
            "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        }
        self._send(
            subject=self._subject(
                "Contact", "Bénéficiaire", "Vous avez un nouveau message 📩"
            ),
            to=orientation.beneficiary_email,
            template="contact-beneficiary.mjml",
            context=context,
            from_email=self._structure_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
            cc=cc,
        )


backend = DoraBackend()


# --- Module-level wrappers preserved for external callers ----------------
#
# `send_orientation_created_to_structure` is imported by orientations/views.py
# and __init__.py; the other `send_orientation_*_to_structure` helpers are
# invoked by the Emplois backend so structure-porteuse emails stay uniform
# regardless of the origin of the orientation.


def send_orientation_created_to_structure(orientation, context=None):
    backend.send_created_to_structure(orientation, context)


def send_orientation_accepted_to_structure(orientation, context=None):
    backend.send_accepted_to_structure(orientation, context)


def send_orientation_rejected_to_structure(orientation, context=None):
    backend.send_rejected_to_structure(orientation, context)


def send_orientation_expired_to_structure(orientation, context):
    backend.send_expired_to_structure(orientation, context)
