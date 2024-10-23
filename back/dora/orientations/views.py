from django.utils import timezone
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dora.core.utils import TRUTHY_VALUES

from .emails import (
    send_message_to_beneficiary,
    send_message_to_prescriber,
    send_orientation_accepted_emails,
    send_orientation_created_emails,
    send_orientation_created_to_structure,
    send_orientation_rejected_emails,
)
from .models import (
    ContactRecipient,
    Orientation,
    OrientationStatus,
    RejectionReason,
    SentContactEmail,
)
from .serializers import OrientationSerializer


class OrientationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        match request.method:
            case "DELETE":
                return False
            case _:
                return True

    def has_object_permission(self, request, view, orientation):
        match request.method:
            case "GET" | "POST" | "PATCH":
                if h := request.query_params.get("h"):
                    return h == orientation.get_query_id_hash()
                return False
            case _:
                return False


class OrientationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrientationSerializer
    permission_classes = [OrientationPermission]
    lookup_field = "query_id"

    def get_queryset(self):
        return Orientation.objects.all()

    def perform_create(self, serializer):
        serializer.is_valid()
        orientation = serializer.save(prescriber=self.request.user)
        send_orientation_created_emails(orientation)

    @action(
        detail=True,
        methods=["post"],
        url_path="validate",
    )
    def validate(self, request, query_id=None):
        orientation = self.get_object()
        prescriber_message = self.request.data.get("message")
        beneficiary_message = self.request.data.get("beneficiary_message")
        orientation.processing_date = timezone.now()
        orientation.status = OrientationStatus.ACCEPTED
        orientation.save()
        send_orientation_accepted_emails(
            orientation, prescriber_message, beneficiary_message
        )
        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
        url_path="reject",
    )
    def reject(self, request, query_id=None):
        orientation = self.get_object()
        message = self.request.data.get("message", "")
        reasons = self.request.data.get("reasons", [])
        orientation.processing_date = timezone.now()
        orientation.status = OrientationStatus.REJECTED
        orientation.save()
        orientation.rejection_reasons.set(
            RejectionReason.objects.filter(value__in=reasons)
        )
        send_orientation_rejected_emails(orientation, message)
        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
        url_path="contact/beneficiary",
    )
    def contact_beneficiary(self, request, query_id=None):
        orientation = self.get_object()
        if not orientation.beneficiary_email:
            raise serializers.ValidationError("Adresse email du bénéficiaire inconnue")
        message = self.request.data.get("message")
        cc_prescriber = self.request.data.get("cc_prescriber") in TRUTHY_VALUES
        cc_referent = self.request.data.get("cc_referent") in TRUTHY_VALUES

        sent_contact_emails = []
        cc = []

        if cc_prescriber:
            cc.append(orientation.prescriber.email)
            sent_contact_emails.append(ContactRecipient.PRESCRIBER)
        if (
            cc_referent
            and orientation.referent_email
            and orientation.referent_email != orientation.prescriber.email
        ):
            cc.append(orientation.referent_email)
            sent_contact_emails.append(ContactRecipient.REFERENT)

        send_message_to_beneficiary(orientation, message, cc)

        SentContactEmail.objects.create(
            orientation=orientation,
            recipient=ContactRecipient.BENEFICIARY,
            carbon_copies=sent_contact_emails,
        )
        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
        url_path="contact/prescriber",
    )
    def contact_prescriber(self, request, query_id=None):
        orientation = self.get_object()
        message = self.request.data.get("message")
        cc_beneficiary = self.request.data.get("cc_beneficiary") in TRUTHY_VALUES
        cc_referent = self.request.data.get("cc_referent") in TRUTHY_VALUES

        sent_contact_emails = []
        cc = []

        if cc_beneficiary and orientation.beneficiary_email:
            cc.append(orientation.beneficiary_email)
            sent_contact_emails.append(ContactRecipient.BENEFICIARY)
        if (
            cc_referent
            and orientation.referent_email
            and orientation.referent_email != orientation.prescriber.email
        ):
            cc.append(orientation.referent_email)
            sent_contact_emails.append(ContactRecipient.REFERENT)

        send_message_to_prescriber(orientation, message, cc)

        SentContactEmail.objects.create(
            orientation=orientation,
            recipient=ContactRecipient.PRESCRIBER,
            carbon_copies=sent_contact_emails,
        )

        return Response(status=204)

    @action(
        detail=True,
        methods=["patch"],
        url_path="refresh",
        permission_classes=[permissions.AllowAny],
    )
    def refresh(self, request, query_id=None):
        # la régénération du hash est le seul point d'entrée "ouvert",
        # pas d'échange d'information, juste une demande traitée côté backend.
        orientation = self.get_object()
        orientation.refresh_query_expiration_date()

        # renvoi de l'e-mail avec un nouveau lien (uniquement pour la structure)
        send_orientation_created_to_structure(orientation)

        return Response(status=204)
