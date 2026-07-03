from django.conf import settings

from .base import OrientationEmailBackend
from .dora import DoraBackend

debug = settings.ORIENTATION_EMAILS_DEBUG


class EmploisBackend(OrientationEmailBackend):
    template_dir = "emplois/"
    role_label = "Emplois "

    def __init__(self):
        # Les mails aux offreurs de services sont toujours ceux de Dora donc
        # il faut utiliser le backend de Dora peu importe la source de l'orientation
        self._dora = DoraBackend()

    def _debug(self):
        return debug

    def _default_from_email(self):
        return ("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL)

    def _contact_from_email(self, orientation):
        return (
            f"{orientation.get_structure_name()} via Les Emplois",
            settings.DEFAULT_FROM_EMAIL,
        )

    # --- Création ---------------------------------------------------------

    def _send_created_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Envoyée", "Prescripteur", "Votre demande a bien été transmise !"
            ),
            to=orientation.prescriber_info.email,
            template="orientation-creation-prescriber.mjml",
            context=context,
            from_email=self._default_from_email(),
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
            template="orientation-creation-referent.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.prescriber_info.email],
        )

    def _send_created_to_beneficiary(self, orientation, context):
        self._send(
            subject=self._subject(
                "Envoyée",
                "Bénéficiaire",
                "Une orientation a été effectuée en votre nom",
            ),
            to=orientation.beneficiary_email,
            template="orientation-creation-beneficiary.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.prescriber_info.email],
        )

    def send_created(self, orientation):
        # Structure email keeps its DORA-branded template + ctx.
        self._dora.send_created_to_structure(orientation)

        context = {
            "orientation": orientation,
            "service_address": self.get_service_address_line(),
        }
        self._send_created_to_prescriber(orientation, context)
        self._send_created_to_referent(orientation, context)
        self._send_created_to_beneficiary(orientation, context)

    # --- Validation --------------------------------------------------------

    def _send_accepted_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Validée", "Prescripteur", "Votre demande a été acceptée ! 🎉"
            ),
            to=orientation.prescriber_info.email,
            template="orientation-accepted-prescriber.mjml",
            context=context,
            from_email=self._default_from_email(),
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
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def _send_accepted_to_beneficiary(self, orientation, context):
        self._send(
            subject=self._subject(
                "Validée", "Bénéficiaire", "Votre demande a été acceptée ! 🎉"
            ),
            to=orientation.beneficiary_email,
            template="orientation-accepted-beneficiary.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def send_accepted(self, orientation, prescriber_message, beneficiary_message):
        self._dora.send_accepted_to_structure(
            orientation,
            self._dora._orientation_accepted_ctx(
                orientation, prescriber_message, beneficiary_message
            ),
        )

        placeholder = "#SERVICE_ADDRESS#"
        service_address = self.get_service_address_line()
        prescriber_message = prescriber_message.replace(placeholder, service_address)
        beneficiary_message = beneficiary_message.replace(placeholder, service_address)

        context = {
            "orientation": orientation,
            "prescriber_message": prescriber_message,
            "beneficiary_message": beneficiary_message,
        }
        self._send_accepted_to_prescriber(orientation, context)
        self._send_accepted_to_referent(orientation, context)
        self._send_accepted_to_beneficiary(orientation, context)

    # --- Refus --------------------------------------------------------

    def _send_rejected_to_beneficiary(self, orientation, context):
        self._send(
            subject=self._subject(
                "Refusée",
                "Bénéficiaire",
                "Votre demande d’orientation a été refusée",
            ),
            to=orientation.beneficiary_email,
            template="orientation-rejected-beneficiary.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def _send_rejected_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Refusée",
                "Prescripteur",
                "Votre demande d’orientation a été refusée",
            ),
            to=orientation.prescriber_info.email,
            template="orientation-rejected-prescriber.mjml",
            context=context,
            from_email=self._default_from_email(),
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
            to=orientation.referent_email,
            template="orientation-rejected-prescriber.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def send_rejected(self, orientation, message, other_details=""):
        self._dora.send_rejected_to_structure(
            orientation, self._dora._orientation_rejected_ctx(orientation, message)
        )

        context = {
            "orientation": orientation,
            "message": message,
            "other_details": other_details,
        }
        self._send_rejected_to_beneficiary(orientation, context)
        self._send_rejected_to_prescriber(orientation, context)
        self._send_rejected_to_referent(orientation, context)

    # --- Expiration ---------------------------------------------------------

    def _send_expired_to_prescriber(self, orientation, context):
        self._send(
            subject=self._subject(
                "Expirée", "Prescripteur", "Votre demande d’orientation a expiré"
            ),
            to=orientation.prescriber_info.email,
            template="orientation-expired-prescriber.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def _send_expired_to_referent(self, orientation, context):
        if not self._has_distinct_referent(orientation):
            return
        self._send(
            subject=self._subject(
                "Expirée",
                "Conseiller référent",
                "Votre demande d’orientation a expiré",
            ),
            to=orientation.referent_email,
            template="orientation-expired-prescriber.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def _send_expired_to_beneficiary(self, orientation, context):
        self._send(
            subject=self._subject(
                "Expirée",
                "Bénéficiaire",
                "Cette demande d’orientation a été annulée",
            ),
            to=orientation.beneficiary_email,
            template="orientation-expired-beneficiary.mjml",
            context=context,
            from_email=self._default_from_email(),
            reply_to=[orientation.get_contact_email()],
        )

    def send_expired(self, orientation, start_date=None):
        self._dora.send_expired_to_structure(
            orientation, self._dora._orientation_expired_ctx(orientation, start_date)
        )

        context = {"orientation": orientation}
        self._send_expired_to_prescriber(orientation, context)
        self._send_expired_to_referent(orientation, context)
        self._send_expired_to_beneficiary(orientation, context)

    # --- Messages de contact -------------------------------------------------

    def send_message_to_prescriber(self, orientation, message, cc):
        structure_name = orientation.get_structure_name()
        context = {"orientation": orientation, "message": message}
        self._send(
            subject=self._subject(
                "Contact",
                "Prescripteur",
                f"Vous avez un nouveau message de la structure {structure_name}",
            ),
            to=orientation.prescriber_info.email,
            template="orientation-contact-prescriber.mjml",
            context=context,
            from_email=self._contact_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
            cc=cc,
        )

    def send_message_to_beneficiary(self, orientation, message, cc):
        structure_name = orientation.get_structure_name()
        context = {
            "orientation": orientation,
            "message": message,
            "structure_name": structure_name,
        }
        self._send(
            subject=self._subject(
                "Contact",
                "Bénéficiaire",
                f"Vous avez un nouveau message de la structure {structure_name}",
            ),
            to=orientation.beneficiary_email,
            template="orientation-contact-beneficiary.mjml",
            context=context,
            from_email=self._contact_from_email(orientation),
            reply_to=[orientation.get_contact_email()],
            cc=cc,
        )


backend = EmploisBackend()
