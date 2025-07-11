import logging
from typing import Dict, List
from urllib.parse import quote

import sib_api_v3_sdk as brevo_api
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException as BrevoApiException

from dora.structures.models import Structure
from dora.users.models import User

"""
L'onboarding d'un utilisateur est maintenant décomposé en 2 parties :
    - pour les utilisateurs en attente de validation,
    - pour les utilisateurs déjà validés.

Il y a également deux nouvelles listes ("routes") Brevo distinctes pour l'envoi des données,
voir dans les settings :
    - `BREVO_ONBOARDING_MEMBER_LIST`
    - `BREVO_ONBOARDING_PUTATIVE_MEMBER_LIST`
"""

logger = logging.getLogger(__name__)

Attributes = Dict[str, str | List[str]]


def _setup_brevo_client() -> brevo_api.ContactsApi | None:
    if not settings.BREVO_ACTIVE:
        logger.warning(
            f"L'API Brevo n'est pas active sur cet environnement {settings.ENVIRONMENT}"
        )
        return

    configuration = brevo_api.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY
    return brevo_api.ContactsApi(brevo_api.ApiClient(configuration))


def _brevo_contact_for_user(
    client: brevo_api.ContactsApi, user: User
) -> brevo_api.GetExtendedContactDetails | None:
    try:
        return client.get_contact_info(user.email)
    except BrevoApiException as exc:
        # l'API Brevo renvoie une erreur 404 si l'utilisateur n'est pas trouvé
        if exc.status != 404:
            raise exc


def _contact_in_brevo_list(
    client: brevo_api.ContactsApi, user: User, brevo_list_id: int
) -> bool:
    try:
        contact = client.get_contact_info(user.email)
    except BrevoApiException as exc:
        # l'API Brevo renvoie une erreur 400 si l'utilisateur n'est pas trouvé
        if exc.status != 400:
            raise exc
    else:
        return brevo_list_id in contact.list_ids

    return False


def _update_brevo_contact(
    client: brevo_api.ContactsApi, user: User, attributes: Attributes
) -> bool:
    contact_attributes = brevo_api.UpdateContact(attributes=attributes)
    try:
        client.update_contact(user.email, contact_attributes)
    except BrevoApiException as exc:
        logger.exception(exc)
        logger.error(
            "Impossible de modifier les attributs pour l'utilisateur %s",
            user.pk,
        )
        return False

    return True


def _add_user_to_brevo_list(
    client: brevo_api.ContactsApi, user: User, brevo_list_id: int
) -> bool:
    try:
        client.add_contact_to_list(
            brevo_list_id,
            brevo_api.AddContactToList(emails=[user.email]),
        )
        logger.info(
            "L'utilisateur #%s a été ajouté à la liste d'onboarding Brevo: %s",
            user.pk,
            brevo_list_id,
        )
    except BrevoApiException as exc:
        logger.exception(exc)
        logger.error(
            "Impossible d'ajouter l'utilisateur #%s à la liste d'onboarding Brevo",
            user.pk,
        )
        return False

    return True


def _remove_from_brevo_list(
    client: brevo_api.ContactsApi, user: User, brevo_list_id: int
) -> bool:
    try:
        client.remove_contact_from_list(
            brevo_list_id, brevo_api.RemoveContactFromList(emails=[user.email])
        )
        logger.info(
            "L'utilisateur #%s a été retiré de la liste Brevo: %s",
            user.pk,
            brevo_list_id,
        )
    except BrevoApiException as exc:
        logger.exception(exc)
        logger.error(
            "Impossible de retirer l'utilisateur #%s de la liste Brevo: %s",
            user.pk,
            brevo_list_id,
        )
        return False

    return True


def _create_brevo_contact(
    client: brevo_api.ContactsApi,
    user: User,
    attributes: Attributes,
    brevo_list_id: int,
) -> bool:
    create_contact = brevo_api.CreateContact(
        email=user.email,
        attributes=attributes,
        list_ids=[brevo_list_id],
        update_enabled=False,
    )

    try:
        api_response = client.create_contact(create_contact)
        logger.info(
            "Utilisateur #%s ajouté en tant que contact à la liste Brevo: %s (%s)",
            user.pk,
            brevo_list_id,
            api_response,
        )
        return True
    except BrevoApiException as e:
        # note : les traces de l'exception peuvent être tronquées sur Sentry
        logger.exception(e)

    return False


def _create_or_update_brevo_contact(
    client: brevo_api.ContactsApi,
    user: User,
    attributes: Attributes,
    brevo_list_id: int,
) -> None:
    contact = _brevo_contact_for_user(client, user)

    if not contact:
        _create_brevo_contact(client, user, attributes, brevo_list_id)
        return

    if not _contact_in_brevo_list(client, user, brevo_list_id):
        if _update_brevo_contact(client, user, attributes):
            _add_user_to_brevo_list(client, user, brevo_list_id)


def onboard_user(user: User, structure: Structure) -> None:
    """
    Onboarding de l'utilisateur pour une structure :
        Déclenché lors du rattachement à une structure.
        L'utilisateur est transformé en 'contact' de l'API Brevo,
        puis rattaché à une liste selon son status (membre ou en attente)
        et son type d'activité.
    """

    client = _setup_brevo_client()
    if not client:
        return

    is_first_admin = not structure.has_admin()
    attributes = {
        "PRENOM": user.first_name,
        "NOM": user.last_name,
        "PROFIL": user.main_activity,
        "IS_ADMIN": structure.is_admin(user),
        "IS_FIRST_ADMIN": is_first_admin,
        "URL_DORA_STRUCTURE": structure.get_frontend_url(),
        "NEED_VALIDATION": structure.is_pending_member(user),
        "NOM_STRUCTURE": structure.name,
        "CONTACT_ADHESION": [admin.email for admin in structure.admins],
        "VILLE": quote(structure.city),
        "CITY_CODE_DORA": structure.city_code,
        "NO_DEPARTEMENT": structure.department,
    }

    is_user_member = structure.is_member(user)

    brevo_list_id = int(
        settings.BREVO_ONBOARDING_MEMBER_LIST
        if is_user_member
        else settings.BREVO_ONBOARDING_PUTATIVE_MEMBER_LIST
    )

    _create_or_update_brevo_contact(client, user, attributes, brevo_list_id)

    # dans le cas d'un utilisateur passé membre, le retirer de la liste des invités
    if is_user_member and _contact_in_brevo_list(
        client, user, settings.BREVO_ONBOARDING_PUTATIVE_MEMBER_LIST
    ):
        # Dans le cas des imports via commande / script,
        # les utilisateurs peuvent ne pas être passés par la liste "invité".
        # Les retirer de la liste sans y vérifier leur présence provoque un log d'erreur,
        # sans conséquence, mais qui alimente quand même les erreurs Sentry.
        _remove_from_brevo_list(
            client, user, int(settings.BREVO_ONBOARDING_PUTATIVE_MEMBER_LIST)
        )
