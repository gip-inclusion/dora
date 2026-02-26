from django.conf import settings
from itoutils.django.nexus.management.base_full_sync import BaseNexusFullSyncCommand

from dora.nexus.sync import serialize_membership, serialize_structure, serialize_user
from dora.structures.models import Structure, StructureMember
from dora.users.models import User


class Command(BaseNexusFullSyncCommand):
    CHUNK_SIZE = settings.NEXUS_SYNC_CHUNK_SIZE
    structure_serializer = staticmethod(serialize_structure)
    user_serializer = staticmethod(serialize_user)
    membership_serializer = staticmethod(serialize_membership)

    def get_structures_queryset(self):
        return Structure.objects.filter(is_obsolete=False).exclude(
            name__icontains="[ND]"
        )

    def get_users_queryset(self):
        return (
            User.objects.filter(
                is_active=True,
                is_staff=False,
            )
            .exclude(email=settings.DORA_BOT_USER)
            .exclude(first_name="")
            .exclude(last_name="")
        )

    def get_memberships_queryset(self):
        return (
            StructureMember.objects.filter(
                user__is_active=True,
                user__is_staff=False,
                structure__is_obsolete=False,
            )
            .exclude(user__email=settings.DORA_BOT_USER)
            .exclude(user__first_name="")
            .exclude(user__last_name="")
        )
