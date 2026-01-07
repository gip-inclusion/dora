from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from furl import furl
from mjml import mjml2html

from dora.core.emails import send_mail
from dora.support.views import StructureAdminViewSet


def send_invitation_reminder(user, structure, notification=False):
    cta_link = furl(settings.FRONTEND_URL) / "auth" / "invitation"
    cta_link.add({"login_hint": iri_to_uri(user.email), "structure": structure.slug})

    if notification:
        cta_link.add(
            {
                "mtm_campaign": "MailsTransactionnels",
                "mtm_keyword": "InvitationaConfirmer",
            }
        )

    context = {
        "user": user,
        "structure": structure,
        "cta_link": cta_link.url,
        "with_dora_info": True,
        "with_legal_info": True,
    }

    send_mail(
        f"Rappel : Acceptez l'invitation à rejoindre {structure.name} sur DORA",
        user.email,
        mjml2html(render_to_string("invitation_reminder.mjml", context)),
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["notification"],
    )


def send_user_without_structure_notification(user, deletion=False):
    # même notification et contexte mais template différent si dernier rappel
    cta_link = furl(settings.FRONTEND_URL) / "auth" / "rattachement"
    cta_link.add(
        {
            "login_hint": iri_to_uri(user.email),
            "mtm_campaign": "MailsTransactionnels",
            "mtm_keyword": "InscritSansStructure",
        }
    )
    context = {
        "user": user,
        "cta_link": cta_link.url,
        "with_legal_info": True,
    }

    send_mail(
        "Dernier rappel avant suppression"
        if deletion
        else "Rappel : Identifiez votre structure sur DORA",
        user.email,
        mjml2html(
            render_to_string(
                "notification_user_without_structure_deletion.mjml"
                if deletion
                else "notification_user_without_structure.mjml",
                context,
            )
        ),
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["notification"],
    )


def send_account_deletion_notification(user):
    # envoyé 30j avant la destruction effective du compte utilisateur
    cta_link = furl(settings.FRONTEND_URL) / "auth" / "connexion"
    cta_link.add(
        {
            "login_hint": iri_to_uri(user.email),
            "mtm_campaign": "MailsTransactionnels",
            "mtm_kwd": "RelanceInactif",
        }
    )
    context = {
        "limit_date": timezone.localdate() + relativedelta(days=30),
        "cta_link": cta_link.url,
    }

    send_mail(
        "DORA - Suppression prochaine de votre compte",
        user.email,
        mjml2html(render_to_string("notification_account_deletion.mjml", context)),
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["notification"],
    )


MAX_STRUCTURES_PER_CATEGORY = 10


def send_weekly_email_to_department_managers(manager):
    # envoyé aux gestionnaires de territoire tous les mercredis
    # avec la liste des structures qui exigent une action de leur part

    relevant_structures = StructureAdminViewSet.get_base_queryset_for_manager(manager)

    all_awaiting_moderation = relevant_structures.filter(
        is_orphan=False, is_waiting=False, awaiting_moderation=True
    )
    all_orphans = relevant_structures.filter(is_orphan=True)
    total_structures_count = all_awaiting_moderation.count() + all_orphans.count()

    awaiting_moderation = all_awaiting_moderation.order_by("name")[
        :MAX_STRUCTURES_PER_CATEGORY
    ].values_list("name", flat=True)
    orphans = all_orphans.order_by("name")[:MAX_STRUCTURES_PER_CATEGORY].values_list(
        "name", flat=True
    )

    cta_link = furl(settings.FRONTEND_URL) / "admin" / "structures"
    context = {
        "structures_awaiting_moderation": awaiting_moderation,
        "structures_without_users": orphans,
        "cta_link": cta_link.url,
        "num_structures": total_structures_count,
    }

    if awaiting_moderation or orphans:
        send_mail(
            "Vous avez des structures à modérer cette semaine",
            manager.email,
            mjml2html(
                render_to_string(
                    "notification_department_manager_structures_requiring_action.mjml",
                    context,
                )
            ),
            from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
            tags=["notification", "gestionnaires"],
        )
