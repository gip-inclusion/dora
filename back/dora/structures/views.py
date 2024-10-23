from data_inclusion.schema import Typologie
from django.db import transaction
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import exceptions, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from dora import onboarding
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.pagination import OptionalPageNumberPagination
from dora.services.enums import ServiceStatus
from dora.structures.constants import RESTRICTED_NATIONAL_LABELS
from dora.structures.emails import send_invitation_email
from dora.structures.models import (
    Structure,
    StructureMember,
    StructureNationalLabel,
    StructurePutativeMember,
    StructureSource,
)
from dora.structures.permissions import (
    StructureMemberPermission,
    StructurePermission,
    StructurePutativeMemberPermission,
)

from .serializers import (
    StructureListSerializer,
    StructureMemberSerializer,
    StructurePutativeMemberSerializer,
    StructureSerializer,
)


class StructureViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StructureSerializer
    permission_classes = [StructurePermission]
    pagination_class = OptionalPageNumberPagination

    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        only_managed = self.request.query_params.get("managed")
        only_pending = self.request.query_params.get("pending")
        only_active = self.request.query_params.get("active")
        search_string = self.request.query_params.get("search", None)

        structures = Structure.objects.select_related("source", "parent").all()

        if search_string:
            structures = structures.filter(name__icontains=search_string)

        if only_managed:
            if not user or not user.is_authenticated:
                return Structure.objects.none()
            if user.is_staff:
                return structures.order_by("-modification_date").distinct()
            elif user.is_manager and user.departments:
                return (
                    structures.filter(department__in=user.departments)
                    .order_by("-modification_date")
                    .distinct()
                )
            else:
                return (
                    structures.filter(membership__user=user)
                    .order_by("-modification_date")
                    .distinct()
                )
        elif only_pending:
            if not user or not user.is_authenticated:
                return Structure.objects.none()
            return (
                structures.filter(putative_membership__user=user)
                .exclude(putative_membership__invited_by_admin=True)
                .order_by("-modification_date")
                .distinct()
            )
        elif only_active:
            qs = (
                structures.filter(services__status=ServiceStatus.PUBLISHED)
                .order_by("-modification_date")
                .distinct()
            )
            return qs
        else:
            return structures.order_by("-modification_date")

    def get_serializer_class(self):
        if self.action == "list":
            return StructureListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        user = self.request.user
        source = (
            StructureSource.objects.get(value="equipe-dora")
            if user.is_staff
            else StructureSource.objects.get(value="porteur")
        )
        structure = serializer.save(
            creator=user,
            last_editor=user,
            source=source,
            modification_date=timezone.now(),
        )
        # When creating a structure, the creator becomes member and administrator of this structure
        StructureMember.objects.create(
            user=user,
            structure=structure,
            is_admin=True,
        )

        send_moderation_notification(
            structure,
            self.request.user,
            "Création",
            ModerationStatus.NEED_INITIAL_MODERATION,
        )

    def perform_update(self, serializer):
        structure = serializer.save(
            last_editor=self.request.user,
            modification_date=timezone.now(),
            has_been_edited=True,
        )
        structure.log_note(self.request.user, "Structure modifiée")


class StructureMemberViewset(viewsets.ModelViewSet):
    serializer_class = StructureMemberSerializer
    permission_classes = [StructureMemberPermission]

    def get_queryset(self):
        user = self.request.user

        # Vérifié par has_permission
        assert user and user.is_authenticated
        # get_queryset ne devrait pas être appelé lors d'une creation
        assert self.action != "create"

        # On ne peut lister les membres que pour une structure donnée
        if self.action == "list":
            structure_slug = self.request.query_params.get("structure")
            if structure_slug is None:
                raise exceptions.ValidationError("?structure is required")
            try:
                structure = Structure.objects.get(slug=structure_slug)
            except Structure.DoesNotExist:
                raise exceptions.NotFound

            if structure.can_view_members(user):
                return StructureMember.objects.filter(
                    structure=structure, user__is_valid=True
                )
            raise exceptions.PermissionDenied

        else:
            # Les superuser ont accès à tous les collaborateurs
            if user.is_staff:
                return StructureMember.objects.all()

            # Les gestionnaires ont accès à tous les collaborateurs de
            # leur département
            elif user.is_manager and user.departments:
                return StructureMember.objects.filter(
                    structure__department__in=user.departments
                )

            # Les membres des structures ont accès à tous leurs collègues
            else:
                user_structures = StructureMember.objects.filter(
                    user_id=user.id
                ).values_list("structure_id", flat=True)
                return StructureMember.objects.filter(structure_id__in=user_structures)


class StructurePutativeMemberViewset(viewsets.ModelViewSet):
    serializer_class = StructurePutativeMemberSerializer
    permission_classes = [StructurePutativeMemberPermission]

    def get_queryset(self):
        user = self.request.user

        # Vérifié par has_permission
        assert user and user.is_authenticated

        # get_queryset ne devrait pas être appelé lors d'une creation
        assert self.action != "create"

        # On ne peut lister les membres que pour une structure donnée
        if self.action == "list":
            structure_slug = self.request.query_params.get("structure")
            if structure_slug is None:
                return StructurePutativeMember.objects.none()
            try:
                structure = Structure.objects.get(slug=structure_slug)
            except Structure.DoesNotExist:
                raise exceptions.NotFound

            if structure.can_view_members(user):
                # On ne veut voir que les utilisateurs qui ont été invités
                # ou qui ont déjà validé leur email
                return StructurePutativeMember.objects.filter(
                    Q(user__is_valid=True) | Q(invited_by_admin=True),
                    structure=structure,
                )

            else:
                raise exceptions.PermissionDenied

        else:
            # Les superusers ont accès à tous les collaborateurs
            if user.is_staff:
                return StructurePutativeMember.objects.filter(
                    Q(user__is_valid=True) | Q(invited_by_admin=True),
                )

            # Les gestionnaires ont accès à tous les collaborateurs de
            # leur département
            elif user.is_manager and user.departments:
                return StructurePutativeMember.objects.filter(
                    Q(user__is_valid=True) | Q(invited_by_admin=True),
                    structure__department__in=user.departments,
                )

            # Les membres des structures ont accès à tous leurs collègues
            else:
                user_structures = StructureMember.objects.filter(
                    user_id=user.id
                ).values_list("structure_id", flat=True)
                return StructurePutativeMember.objects.filter(
                    structure_id__in=user_structures
                )

    @action(
        detail=True,
        methods=["post"],
        url_path="resend-invite",
        permission_classes=[permissions.IsAuthenticated],
    )
    def resend_invite(self, request, pk):
        try:
            member = StructurePutativeMember.objects.get(id=pk)
        except StructurePutativeMember.DoesNotExist:
            raise exceptions.NotFound
        structure = member.structure
        request_user = request.user
        if not structure.can_edit_members(request.user):
            raise exceptions.PermissionDenied

        send_invitation_email(
            member,
            request_user.get_full_name(),
        )
        return Response(status=201)

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel-invite",
        permission_classes=[permissions.IsAuthenticated],
    )
    # TODO: pourquoi ce n'est pas juste un DELETE ?
    def cancel_invite(self, request, pk):
        try:
            member = StructurePutativeMember.objects.get(id=pk)
        except StructurePutativeMember.DoesNotExist:
            raise exceptions.NotFound
        # Ensure the requester is admin of the structure, manager, or superuser
        structure = member.structure
        if not structure.can_edit_members(request.user):
            raise exceptions.PermissionDenied

        member.delete()
        return Response(status=201)

    @action(
        detail=True,
        methods=["post"],
        url_path="accept-membership-request",
        permission_classes=[permissions.IsAuthenticated],
    )
    def accept_membership_request(self, request, pk):
        # TODO: add tests
        try:
            pm = StructurePutativeMember.objects.get(
                id=pk, user__is_valid=True, user__is_active=True
            )
        except StructurePutativeMember.DoesNotExist:
            raise exceptions.NotFound
        # Ensure the requester is admin of the structure, or superuser
        structure = pm.structure
        request_user = request.user
        if not structure.can_edit_members(request_user):
            raise exceptions.PermissionDenied

        new_member = pm.user

        with transaction.atomic(durable=True):
            membership = StructureMember.objects.create(
                user=pm.user,
                structure=pm.structure,
                is_admin=pm.is_admin,
            )
            pm.delete()
            membership.notify_access_granted()

        # À ce point, il peut être nécessaire de déclencher un onboarding :
        # la *première* acceptation en tant que membre d'une structure déclenche
        # l'inscription à une liste Brevo.
        if new_member.membership.count() == 1:
            # on vient d'enregistrer le nouveau membre (1 seule structure)
            onboarding.onboard_user(new_member, structure)

        return Response(status=201)

    @action(
        detail=True,
        methods=["post"],
        url_path="reject-membership-request",
        permission_classes=[permissions.IsAuthenticated],
    )
    def reject_membership_request(self, request, pk):
        # TODO: add tests
        try:
            pm = StructurePutativeMember.objects.get(id=pk)
        except StructurePutativeMember.DoesNotExist:
            raise exceptions.NotFound
        # Ensure the requester is admin of the structure, or superuser
        structure = pm.structure
        request_user = request.user
        if not structure.can_edit_members(request_user):
            raise exceptions.PermissionDenied

        pm.notify_access_rejected()
        pm.delete()

        return Response(status=201)


@api_view()
@permission_classes([permissions.AllowAny])
def siret_was_claimed(request, siret):
    structure = get_object_or_404(Structure.objects.all(), siret=siret)
    serializer = StructureSerializer(structure, context={"request": request})
    return Response(serializer.data)


@api_view()
@permission_classes([permissions.AllowAny])
def options(request):
    labels = StructureNationalLabel.objects.all().order_by("label")
    result = {
        "typologies": Typologie.as_dict_list(),
        "national_labels": [{"value": c.value, "label": c.label} for c in labels],
        "sources": [
            {"value": c.value, "label": c.label}
            for c in StructureSource.objects.all().order_by("label")
        ],
        # les labels nationaux font l'objet d'une curation : voir `.constants`
        "restricted_national_labels": [
            {"value": c.value, "label": c.label}
            for c in labels
            if c.value in RESTRICTED_NATIONAL_LABELS
        ],
    }
    return Response(result)
