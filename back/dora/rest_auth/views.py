import logging

from django.db import transaction
from django.http.response import Http404
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import exceptions, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import dora.onboarding as onboarding
from dora.core.constants import SIREN_FRANCE_TRAVAIL
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.sirene.models import Establishment
from dora.structures.models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
    StructureSource,
)
from dora.structures.serializers import StructureSerializer
from dora.users.models import User

from ..structures.emails import send_invitation_email
from .serializers import JoinStructureSerializer, TokenSerializer, UserInfoSerializer

logger = logging.getLogger(__name__)


def update_last_login(user):
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])


def _set_user_has_accepted_cgu(user, cgu_version):
    if cgu_version not in user.cgu_versions_accepted:
        user.cgu_versions_accepted.update({cgu_version: timezone.now().isoformat()})
        user.save(update_fields=["cgu_versions_accepted"])


@sensitive_post_parameters(["key"])
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def user_info(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    key = serializer.validated_data["key"]
    try:
        user, token = TokenAuthentication().authenticate_credentials(key)
    except exceptions.AuthenticationFailed:
        raise Http404

    update_last_login(user)

    return Response(UserInfoSerializer(user, context={"token": token}).data, status=200)


def _create_structure(establishment, user, reason):
    try:
        structure = Structure.objects.get(siret=establishment.siret)
    except Structure.DoesNotExist:
        structure = Structure.objects.create_from_establishment(establishment)
        structure.creator = user
        structure.last_editor = user
        structure.source = StructureSource.objects.get(value="porteur")
        structure.save()
        send_moderation_notification(
            structure,
            user,
            reason,
            ModerationStatus.VALIDATED,
        )
    return structure


def _is_member_of_structure(structure, user):
    try:
        StructureMember.objects.get(user=user, structure=structure)
        return True
    except StructureMember.DoesNotExist:
        return False


def _add_user_to_adminless_structure(structure, user):
    add_as_admin = True
    # Si l'utilisateur a été invité (a priori par un superuser), on supprime l'invitation
    try:
        pm = StructurePutativeMember.objects.get(
            user=user,
            structure=structure,
        )
        add_as_admin = pm.is_admin
        pm.delete()
    except StructurePutativeMember.DoesNotExist:
        pass

    # Puis on l'ajoute comme collaborateur
    # (admin par defaut, sauf s'il a été invité comme utilisateur normal)
    StructureMember.objects.create(
        user=user, structure=structure, is_admin=add_as_admin
    )
    send_moderation_notification(
        structure,
        user,
        "Premier administrateur ajouté (par lui-même)",
        ModerationStatus.NEED_INITIAL_MODERATION,
    )


def _add_user_to_structure_or_waitlist(structure, user):
    # Si l'utilisateur a été invité, on le valide directement
    try:
        pm = StructurePutativeMember.objects.get(
            user=user,
            structure=structure,
            invited_by_admin=True,
        )

        membership = StructureMember.objects.create(
            user=pm.user,
            structure=pm.structure,
            is_admin=pm.is_admin,
        )
        pm.delete()
        membership.notify_admins_invitation_accepted()
    except StructurePutativeMember.DoesNotExist:
        # Sinon on le met en liste d'attente, ou on re-notifie l'administrateur s'il y était déjà
        pm, _created = StructurePutativeMember.objects.get_or_create(
            user=user,
            structure=structure,
            is_admin=False,
            defaults={"invited_by_admin": False},
        )
        pm.notify_admin_access_requested()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def join_structure(request):
    user = request.user
    serializer = JoinStructureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    establishment = data.get("establishment")
    structure = data.get("structure")
    siret = establishment.siret if establishment else structure.siret
    if (
        siret
        and siret.startswith(SIREN_FRANCE_TRAVAIL)
        and user.email.split("@")[1]
        not in (
            "pole-emploi.fr",
            "francetravail.fr",
            "beta.gouv.fr",
        )
    ):
        raise exceptions.PermissionDenied(
            "Seuls les agents France Travail peuvent se rattacher à une agence France Travail"
        )

    if establishment:
        structure = _create_structure(
            establishment, user, "Structure créée lors d'une inscription"
        )

    structure_has_admin = structure.has_admin()

    if data.get("cgu_version"):
        _set_user_has_accepted_cgu(user, data.get("cgu_version"))

    if _is_member_of_structure(structure, user):
        return Response(
            StructureSerializer(structure, context={"request": request}).data
        )

    # on teste au préalable si l'utilisateur était membre de la structure
    # pour effectuer l'onboarding *après* le rattachement
    was_already_member_of_a_structure = (
        StructureMember.objects.filter(user=user).exists()
        or StructurePutativeMember.objects.filter(
            user=user, invited_by_admin=False
        ).exists()
    )

    if not structure_has_admin:
        _add_user_to_adminless_structure(structure, user)
    else:
        _add_user_to_structure_or_waitlist(structure, user)

    # point de départ de l'onboarding : l'utilisateur demande à rejoindre
    # ou rejoint effectivement une structure (en tant que premier admin)
    if not was_already_member_of_a_structure:
        onboarding.onboard_user(user, structure)

    return Response(StructureSerializer(structure, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic
def invite_first_admin(request):
    inviter = request.user
    if not (inviter.is_staff or (inviter.is_manager and inviter.departments)):
        raise exceptions.PermissionDenied
    siret = request.data.get("siret")
    if not siret:
        raise ValidationError("SIRET requis")
    invitee_email = request.data.get("invitee_email")
    if not invitee_email:
        raise ValidationError("invitee_email requis")
    try:
        establishment = Establishment.objects.get(siret=siret)
    except Establishment.DoesNotExist:
        raise ValidationError("SIRET inconnu")

    if (
        siret
        and siret.startswith(SIREN_FRANCE_TRAVAIL)
        and invitee_email.split("@")[1]
        not in (
            "pole-emploi.fr",
            "francetravail.fr",
            "beta.gouv.fr",
        )
    ):
        raise exceptions.PermissionDenied(
            "Seuls les agents France Travail peuvent se rattacher à une agence France Travail"
        )

    structure = _create_structure(
        establishment, inviter, "Structure créée lors d'une invitation"
    )

    if structure.has_admin():
        raise ValidationError("Cette structure a déjà un administrateur")
    else:
        try:
            invitee = User.objects.get_by_email(invitee_email)
        except User.DoesNotExist:
            invitee = User.objects.create_user(
                invitee_email,
            )
        try:
            StructurePutativeMember.objects.get(
                user=invitee, structure=structure
            ).delete()
        except StructurePutativeMember.DoesNotExist:
            pass

        try:
            member = StructureMember.objects.get(user=invitee, structure=structure)
            if not member.is_admin:
                member.is_admin = True
                member.save()
                structure.admin_already_invited = True
                structure.save(update_fields=["admin_already_invited"])
        except StructureMember.DoesNotExist:
            member = StructurePutativeMember.objects.create(
                user=invitee,
                structure=structure,
                invited_by_admin=True,
                is_admin=True,
            )
            structure.admin_already_invited = True
            structure.save(update_fields=["admin_already_invited"])
            send_invitation_email(
                member,
                inviter.get_full_name(),
            )

    return Response(
        StructureSerializer(structure, context={"request": request}).data, status=201
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def accept_cgu(request):
    cgu_version = request.data.get("cgu_version")

    if not cgu_version:
        return Response(status=400)

    _set_user_has_accepted_cgu(request.user, cgu_version)
    return Response(status=204)
