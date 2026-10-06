import logging

logger = logging.getLogger(__name__)


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
        "description": structure.description,
        "opening_hours": structure.opening_hours or "",
        "accessibility": structure.accesslibre_url or "",
        "source_link": structure.get_absolute_url(),
    }


def serialize_membership(membership):
    return {
        "id": str(membership.pk),
        "user_id": str(membership.user_id),
        "structure_id": str(membership.structure_id),
        "role": "ADMINISTRATOR" if membership.is_admin else "COLLABORATOR",
    }
