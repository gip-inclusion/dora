import logging
from urllib.parse import quote

import sib_api_v3_sdk as sib_api
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException as SibApiException

from dora.structures.models import Structure
from dora.users.enums import MainActivity
from dora.users.models import User

"""
L'onboarding d'un utilisateur est maintenant décomposé en 2 parties :
    - pour les utilisateurs en attente de validation,
    - pour les utilisateurs déjà validés.

Le process d'onboarding fait essentiellement appel à l'API SendInBlue/Brevo et
devrait être distinct du modèle utilisateur et/ou structure, d'ou l'implémentation
dans un module distinct `dora.onboarding`.

Il y a également deux nouvelles listes ("routes") SIB distinctes pour l'envoi des données,
voir dans les settings :
    - `SIB_ONBOARDING_MEMBER_LIST`
    - `SIB_ONBOARDING_PUTATIVE_MEMBER_LIST`

La route/liste par défaut (`SIB_ONBOARDING_LIST`) reste encore active pour tous les utilisateurs
offreurs ou d'une autre catégorie.
"""

logger = logging.getLogger(__name__)


# note :
# on mélange ici de l'API SIB et du comportement métier (déclenchement de l'onboarding).
# Les fonctions "privées" seront déplacées vers l'app `dora.external` qui comportera les
# éléments de connexion vers des systèmes tiers (API FT, Cheops, Tipimail ...).


def _setup_sib_client() -> sib_api.ContactsApi | None:
    # retourne une instance de client d'API SIB
    # TODO: à bouger vers `external` une fois validé
    if not settings.SIB_ACTIVE:
        logger.warning(
            "L'API SiB n'est pas active sur cet environnement (dev / test ?)"
        )
        return

    configuration = sib_api.Configuration()
    configuration.api_key["api-key"] = settings.SIB_API_KEY
    return sib_api.ContactsApi(sib_api.ApiClient(configuration))


def _sib_contact_for_user(
    client: sib_api.ContactsApi, user: User
) -> sib_api.GetExtendedContactDetails | None:
    # on vérifie l'existence de l'utilisateur en tant que contact Brevo / SiB
    try:
        # l'API SiB renvoie une erreur 404 si l'utilisateur n'est pas trouvé
        return client.get_contact_info(user.email)
    except SibApiException as exc:
        # 404 : l'utilisateur n'existe pas dans SiB, on peut continuer
        if exc.status != 404:
            # sinon il s'agit d'une autre erreur SiB
            raise exc


def _contact_in_sib_list(
    client: sib_api.ContactsApi, user: User, sib_list_id: int
) -> bool:
    # vérifie si l'utilisateur est déjà dans la liste SIB donnée

    # on vérifie d'abord l'existence de l'utilisateur en tant que contact Brevo
    try:
        # l'API SiB renvoie une erreur 400 si l'utilisateur n'est pas trouvé
        contact = client.get_contact_info(user.email)
    except SibApiException as exc:
        # 404 : l'utilisateur n'existe pas dans SiB, on peut continuer
        if exc.status != 400:
            # sinon il s'agit d'une autre erreur SiB
            raise exc
    else:
        # on vérifie l'appartenance à la liste SIB ciblée
        if sib_list_id in contact.list_ids:
            # rien de plus à faire : l'utilisateur appartient déjà à la liste
            logger.warning(
                "L'utilisateur #%s est déja membre de la liste SiB: %s",
                user.pk,
                sib_list_id,
            )
            return True

    return False


def _update_sib_contact(
    client: sib_api.ContactsApi, user: User, attributes: dict
) -> bool:
    # création/ maj des attributs de contact SiB pour l'utilisateur
    contact_attributes = sib_api.UpdateContact(attributes=attributes)
    try:
        client.update_contact(user.email, contact_attributes)
    except SibApiException as exc:
        logger.exception(exc)
        logger.error(
            "Impossible de modifier les attributs pour l'utilisateur %s",
            user.pk,
        )
        return False

    return True


def _add_user_to_sib_list(
    client: sib_api.ContactsApi, user: User, sib_list_id: int
) -> bool:
    # rattachement de l'utilisateur à la liste SiB cible
    try:
        client.add_contact_to_list(
            sib_list_id,
            sib_api.AddContactToList(emails=[user.email]),
        )
        logger.info(
            "L'utilisateur #%s a été ajouté à la liste d'onboarding SiB: %s",
            user.pk,
            sib_list_id,
        )
    except SibApiException as exc:
        logger.exception(exc)
        logger.error(
            "Impossible d'ajouter l'utilisateur #%s à la liste d'onboarding SiB",
            user.pk,
        )
        return False

    return True


def _remove_from_sib_list(
    client: sib_api.ContactsApi, user: User, sib_list_id: int
) -> bool:
    # retire un utilisateur donné d'une liste SiB
    try:
        client.remove_contact_from_list(
            sib_list_id, sib_api.RemoveContactFromList(emails=[user.email])
        )
        logger.info(
            "L'utilisateur #%s a été retiré de la liste SiB: %s", user.pk, sib_list_id
        )
    except SibApiException as exc:
        logger.exception(exc)
        logger.error(
            "Impossible de retirer l'utilisateur #%s de la liste SiB: %s",
            user.pk,
            sib_list_id,
        )
        return False

    return True


def _create_sib_contact(
    client: sib_api.ContactsApi, user: User, attributes: dict, sib_list_id: int
) -> bool:
    # comme toujours avec l'API SiB, on droit créer un objet métier avant de le transmettre
    create_contact = sib_api.CreateContact(
        email=user.email,
        attributes=attributes,
        list_ids=[sib_list_id],
        update_enabled=False,
    )

    try:
        api_response = client.create_contact(create_contact)
        logger.info(
            "Utilisateur #%s ajouté en tant que contact à la liste SiB: %s (%s)",
            user.pk,
            sib_list_id,
            api_response,
        )
        return True
    except SibApiException as e:
        # note : les traces de l'exception peuvent être tronquées sur Sentry
        logger.exception(e)

    return False


def _create_or_update_sib_contact(
    client: sib_api.ContactsApi, user: User, attributes: dict, sib_list_id: int
):
    # On vérifie d'abord si le contact existe
    # (les appels d'API sont différents pour la création et la maj).
    contact = _sib_contact_for_user(client, user)

    if not contact:
        # meilleur des cas : création et affectation à la liste en une passe
        contact = _create_sib_contact(client, user, attributes, sib_list_id)
        return

    # le contact existe, on vérifie si il est déjà rattaché à la liste
    if not _contact_in_sib_list(client, user, sib_list_id):
        # si l'utilisateur existe mais n'est pas rattaché :
        # on mets à jour les attributs du contact (pas possible en une étape à date)
        if _update_sib_contact(client, user, attributes):
            # on rattache le contact à la liste SiB voulue
            _add_user_to_sib_list(client, user, sib_list_id)

    # à ce point, l'utilisateur est déjà onboardé / rattaché, rien d'autre à faire


def onboard_user(user: User, structure: Structure):
    """
    Onboarding de l'utilisateur pour une structure :
        Déclenché lors du rattachement à une structure.
        L'utilisateur est transformé en 'contact' de l'API Brevo / SiB,
        puis rattaché à une liste selon son status (membre ou en attente)
        et son type d'activité.
    """

    client = _setup_sib_client()
    if not client:
        return

    # attributs communs à toute les "routes" d'onboarding
    is_first_admin = not structure.has_admin()
    attributes = {
        "PRENOM": user.first_name,
        "NOM": user.last_name,
        "PROFIL": user.main_activity,
        "IS_ADMIN": structure.is_admin(user),
        "IS_FIRST_ADMIN": is_first_admin,
        "URL_DORA_STRUCTURE": structure.get_frontend_url(),
        "NEED_VALIDATION": structure.is_pending_member(user),
    }

    # détermination de la liste SiB
    match user.main_activity:
        case MainActivity.OFFREUR | MainActivity.AUTRE:
            # process "standard", on utilise la liste principale
            sib_list_id = settings.SIB_ONBOARDING_LIST
            admin_contact = structure.get_most_recently_active_admin()
            attributes |= {
                "CONTACT_ADHESION": admin_contact.user.get_safe_name()
                if admin_contact and not is_first_admin
                else ""
            }
        case MainActivity.ACCOMPAGNATEUR | MainActivity.ACCOMPAGNATEUR_OFFREUR:
            # pour les accompagnateurs et accompagnateurs + offreurs :
            sib_list_id = (
                settings.SIB_ONBOARDING_MEMBER_LIST
                if user in structure.members.all()
                else settings.SIB_ONBOARDING_PUTATIVE_MEMBER_LIST
            )
            attributes |= {
                "NOM_STRUCTURE": structure.name,
                "CONTACT_ADHESION": [admin.email for admin in structure.admins],
                "VILLE": quote(structure.city),
                "CITY_CODE_DORA": structure.city_code,
                "NO_DEPARTEMENT": structure.department,
            }
        case _:
            logger.error(
                "Type d'activité inconnue pour l'utilisateur #%s (%s)",
                user.pk,
                user.main_activity,
            )
            return

    if not sib_list_id:
        logger.error(
            "Impossible de déterminer la liste SiB (variables d'environnement ?)"
        )

    sib_list_id = int(sib_list_id)

    # création ou maj du contact SiB
    _create_or_update_sib_contact(client, user, attributes, sib_list_id)

    # dans le cas d'un utilisateur passé membre, le retirer de la liste des invités
    if sib_list_id == int(settings.SIB_ONBOARDING_MEMBER_LIST):
        if _contact_in_sib_list(client, user, sib_list_id):
            # Dans le cas des imports via commande / script,
            # les utilisateurs peuvent ne pas être passés par la liste "invité".
            # Les retirer de la liste sans y vérifier leur présense provoque un log d'erreur,
            # sans conséquence, mais qui alimente quand même les erreurs Sentry.
            _remove_from_sib_list(
                client, user, int(settings.SIB_ONBOARDING_PUTATIVE_MEMBER_LIST)
            )
