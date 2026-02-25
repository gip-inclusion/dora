import logging

from django.conf import settings
from itoutils.django.nexus.api import NexusAPIClient, NexusAPIException

logger = logging.getLogger(__name__)


USER_TRACKED_FIELDS = [
    "id",
    "main_activity",
    "first_name",
    "last_name",
    "email",
    "last_login",
    "is_active",
]


def serialize_user(user):
    return {
        "id": str(user.pk),
        "kind": user.main_activity,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": "",
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "auth": "PRO_CONNECT" if user.sub_pc else "MAGIC_LINK",
    }


def sync_users(users):
    if settings.NEXUS_API_BASE_URL:
        try:
            NexusAPIClient().send_users([serialize_user(user) for user in users])
        except NexusAPIException:
            pass  # The client already logged the error, we don't want to crash if we can't connect to Nexus
        except Exception:
            logger.exception("Nexus: failed to sync users")


def delete_users(user_pks):
    if settings.NEXUS_API_BASE_URL:
        try:
            NexusAPIClient().delete_users(user_pks)
        except NexusAPIException:
            pass  # The client already logged the error, we don't want to crash if we can't connect to Nexus
        except Exception:
            logger.exception("Nexus: failed to delete users")


STRUCTURE_TRACKED_FIELDS = [
    "typology",
    "siret",
    "name",
    "phone",
    "email",
    "address1",
    "address2",
    "postal_code",
    "city",
    "department",
    "url",
    "full_desc",
    "is_obsolete",
    "accesslibre_url",
    "opening_hours",
]


def serialize_structure(structure):
    return {
        "id": str(structure.pk),
        "kind": structure.typology,
        "siret": structure.siret,
        "name": structure.name,
        "phone": structure.phone,
        "email": structure.email,
        "address_line_1": structure.address1,
        "address_line_2": structure.address2,
        "post_code": structure.postal_code,
        "city": structure.city,
        "department": structure.department,
        "website": structure.url,
        "description": structure.full_desc,
        "opening_hours": structure.opening_hours or "",
        "accessibility": structure.accesslibre_url or "",
        "source_link": structure.get_absolute_url(),
    }


def sync_structues(structures):
    if settings.NEXUS_API_BASE_URL:
        try:
            NexusAPIClient().send_structures(
                [serialize_structure(structure) for structure in structures]
            )
        except NexusAPIException:
            pass  # The client already logged the error, we don't want to crash if we can't connect to Nexus
        except Exception:
            logger.exception("Nexus: failed to sync siaes")


def delete_structures(structure_pks):
    if settings.NEXUS_API_BASE_URL:
        try:
            NexusAPIClient().delete_structures(structure_pks)
        except NexusAPIException:
            pass  # The client already logged the error, we don't want to crash if we can't connect to Nexus
        except Exception:
            logger.exception("Nexus: failed to delete siaes")


MEMBERSHIP_TRACKED_FIELDS = [
    "user_id",
    "structure_id",
    "is_admin",
]


def serialize_membership(membership):
    return {
        "id": str(membership.pk),
        "user_id": str(membership.user_id),
        "structure_id": str(membership.structure_id),
        "role": "ADMINISTRATOR" if membership.is_admin else "COLLABORATOR",
    }


def sync_memberships(memberships):
    if settings.NEXUS_API_BASE_URL:
        try:
            NexusAPIClient().send_memberships(
                [serialize_membership(membership) for membership in memberships]
            )
        except NexusAPIException:
            pass  # The client already logged the error, we don't want to crash if we can't connect to Nexus
        except Exception:
            logger.exception("Nexus: failed to sync siaeusers")


def delete_memberships(membership_pks):
    if settings.NEXUS_API_BASE_URL:
        try:
            NexusAPIClient().delete_memberships(membership_pks)
        except NexusAPIException:
            pass  # The client already logged the error, we don't want to crash if we can't connect to Nexus
        except Exception:
            logger.exception("Nexus: failed to delete siaeusers")
