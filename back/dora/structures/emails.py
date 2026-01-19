from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from furl import furl
from mjml import mjml2html

from dora.core.emails import send_mail


def send_invitation_email(member, inviter_name):
    structure = member.structure
    invitation_link = furl(settings.FRONTEND_URL).add(
        path="/auth/invitation",
        args={
            "login_hint": iri_to_uri(member.user.email),
            "structure": structure.slug,
        },
    )
    params = {
        "recipient_email": member.user.email,
        "recipient_name": member.user.get_short_name(),
        "inviter_name": inviter_name,
        "structure": structure,
        "cta_link": invitation_link,
        "with_legal_info": True,
        "with_dora_info": True,
    }
    body = mjml2html(render_to_string("invitation.mjml", params))

    send_mail(
        "[DORA] Votre invitation sur DORA",
        member.user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["invitation"],
    )


def send_france_travail_invitation_email(member, inviter_name):
    structure = member.structure
    invitation_link = furl(settings.FRONTEND_URL).add(
        path="/auth/invitation",
        args={
            "login_hint": iri_to_uri(member.user.email),
            "structure": structure.slug,
        },
    )
    params = {
        "recipient_email": member.user.email,
        "recipient_name": member.user.get_short_name(),
        "inviter_name": inviter_name,
        "structure": structure,
        "cta_link": invitation_link,
        "with_legal_info": True,
        "with_dora_info": True,
    }
    body = mjml2html(render_to_string("invitation_pe.mjml", params))

    send_mail(
        f"Rejoignez la structure «{structure.name}» sur DORA",
        member.user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["invitation"],
    )


def send_invitation_accepted_notification(member, admin_user):
    params = {
        "recipient_email": admin_user.email,
        "recipient_name": admin_user.get_short_name(),
        "new_member_full_name": member.user.get_full_name(),
        "new_member_email": member.user.email,
        "structure_name": member.structure.name,
    }

    body = render_to_string("notification-invitation-accepted.html", params)

    send_mail(
        "[DORA] Invitation acceptée",
        admin_user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["invitation-accepted"],
    )


def send_access_requested_notification(member, admin_user):
    params = {
        "recipient_email": admin_user.email,
        "recipient_name": admin_user.get_short_name(),
        "new_member_full_name": member.user.get_full_name(),
        "new_member_email": member.user.email,
        "structure_name": member.structure.name,
        "cta_link": f"{settings.FRONTEND_URL}/structures/{member.structure.slug}",
    }

    body = render_to_string("notification-access-request.html", params)

    send_mail(
        "[DORA] Demande d’accès à votre structure",
        admin_user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["access-request"],
    )


def send_access_granted_notification(member):
    params = {
        "structure_name": member.structure.name,
        "cta_link": f"{settings.FRONTEND_URL}/structures/{member.structure.slug}",
    }

    body = render_to_string("notification-access-granted.html", params)

    send_mail(
        "[DORA] Accès accordé",
        member.user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["access-granted"],
    )


def send_access_rejected_notification(member):
    params = {
        "structure_name": member.structure.name,
    }

    body = render_to_string("notification-access-rejected.html", params)

    send_mail(
        "[DORA] Accès refusé",
        member.user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["access-rejected"],
    )


def send_branch_created_notification(structure, branch, admin_user):
    params = {
        "recipient_email": admin_user.email,
        "recipient_name": admin_user.get_short_name(),
        "structure_name": structure.name,
        "cta_link": f"{settings.FRONTEND_URL}/structures/{branch.slug}",
        "branch_name": branch.name,
    }

    body = render_to_string("notification-branch-created.html", params)

    send_mail(
        "[DORA] Votre antenne a été créée",
        admin_user.email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["branch-created"],
    )


def send_orphan_structure_notification(structure):
    # notification aux structures "orphelines" (pas de membre actif)
    cta_link = furl(settings.FRONTEND_URL) / "auth" / "invitation"
    cta_link.add(
        {
            "structure": structure.slug,
            "mtm_campaign": "MailsTransactionnels",
            "mtm_kwd": "InvitationStructuresOrphelines",
        }
    )
    context = {
        "structure": structure,
        "dora_doc_link": "https://aide.dora.inclusion.gouv.fr/fr/",
        "webinar_link": "https://app.livestorm.co/itou/dora-presentation-et-prise-en-main-de-loutil",
        "cta_link": cta_link.url,
    }

    send_mail(
        f"Votre structure n’a pas encore de membre actif sur DORA ({structure.name})",
        structure.email,
        mjml2html(render_to_string("notification-orphan-structure.mjml", context)),
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["notification"],
    )


def send_admin_invited_users_20_notification(structure, user):
    # utilisateurs invités en attente :
    # notification envoyée aux admins de la structure - 20j
    for admin in structure.admins:
        context = {
            "structure": structure,
            "user": user,
            "admin": admin,
            "contact_link": "https://aide.dora.inclusion.gouv.fr/",
            "help_link": "https://aide.dora.inclusion.gouv.fr/fr/article/gerer-le-compte-de-ses-collaborateurs-en-tant-quadministrateur-xkonvm/",
        }
        send_mail(
            "Invitation non acceptée : Action requise",
            admin.email,
            mjml2html(
                render_to_string("notification-invitation-stalled-20.mjml", context)
            ),
            from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
            tags=["notification"],
        )


def send_admin_invited_users_90_notification(structure, user):
    # utilisateurs invités en attente :
    # notification envoyée aux admins de la structure - 90j
    for admin in structure.admins:
        context = {
            "structure": structure,
            "user": user,
            "admin": admin,
        }
        send_mail(
            "Action requise : une de vos invitations sera bientôt désactivée",
            admin.email,
            mjml2html(
                render_to_string("notification-invitation-stalled-90.mjml", context)
            ),
            from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
            tags=["notification"],
        )


def send_admin_self_invited_users_notification(structure, user):
    # rattachements en attente :
    # notification envoyée au admin de la structure
    next_link = furl(f"/structures/{structure.slug}/collaborateurs")

    for admin in structure.admins:
        cta_link = furl(settings.FRONTEND_URL) / "auth" / "connexion"
        cta_link.add({"next": next_link, "login_hint": admin.email})
        cta_link.add(
            {
                "mtm_campaign": "MailsTransactionnels",
                "mtm_kwd": "RattachStructureaValider",
            }
        )

        context = {
            "structure": structure,
            "user": user,
            "admin": admin,
            "cta_link": cta_link.url,
            "contact_link": "https://aide.dora.inclusion.gouv.fr/",
            "help_link": "https://aide.dora.inclusion.gouv.fr/fr/article/gerer-le-compte-de-ses-collaborateurs-en-tant-quadministrateur-xkonvm/",
        }
        send_mail(
            "Rappel : Demande de rattachement en attente",
            admin.email,
            mjml2html(
                render_to_string("notification-self-invited-users.mjml", context)
            ),
            from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
            tags=["notification"],
        )


def send_structure_activation_notification(structure):
    # notification envoyée aux administrateurs de structure
    # pour une première activation de service
    next_link = f"/structures/{structure.slug}/services"
    context = {
        "structure": structure,
        "dora_doc_link": "https://aide.dora.inclusion.gouv.fr/fr/article/referencer-son-offre-de-service-xpivaw/",
        "webinar_link": "https://app.livestorm.co/itou/dora-presentation-et-prise-en-main-de-loutil",
    }

    # aux admins inscrits depuis plus d'un mois
    for membership in structure.membership.filter(
        is_admin=True, creation_date__lt=timezone.now() - relativedelta(months=1)
    ):
        admin = membership.user
        cta_link = furl(settings.FRONTEND_URL) / "auth" / "connexion"
        cta_link.add(
            {
                "login_hint": iri_to_uri(admin.email),
                "mtm_campaign": "MailsTransactionnels",
                "mtm_kwd": "RelanceActivationService",
                "next": next_link,
            }
        )
        context |= {"cta_link": cta_link}
        send_mail(
            f"Votre structure n’a pas encore publié de service sur DORA ({structure.name})",
            admin.email,
            mjml2html(
                render_to_string("notification-service-activation.mjml", context),
            ),
            from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
            tags=["notification"],
        )


def send_moderation_rejected_notification(structure, reason: str):
    eula_link = furl(settings.FRONTEND_URL) / "cgu"
    for user in structure.members.all().union(structure.putative_members.all()):
        context = {
            "structure": structure,
            "user": user,
            "reason": reason,
            "eula_link": eula_link,
        }
        send_mail(
            "[DORA] Décision de modération concernant votre compte",
            user.email,
            mjml2html(
                render_to_string("notification-moderation-rejected.mjml", context)
            ),
            from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
            tags=["notification"],
        )
