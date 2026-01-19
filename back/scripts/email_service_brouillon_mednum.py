from itertools import chain

from django.conf import settings
from django.template.loader import render_to_string
from furl import furl
from mjml import mjml2html

from dora.core.emails import send_mail
from dora.services.enums import ServiceStatus
from dora.services.models import Service

"""
Envoi "one-shot" d'une notification par e-mail aux admins de structures
ayant des services "MEDNUM" en brouillons.
"""

mednum_draft_services = Service.objects.filter(
    status=ServiceStatus.DRAFT, data_inclusion_source__contains="mediation-numerique"
).select_related("structure")
target_structures = [service.structure for service in mednum_draft_services]
admins = list(set(chain(*[structure.admins for structure in target_structures])))

if not mednum_draft_services:
    print("Aucun service MEDNUM en brouillon.")
    exit()


def send_service_draft_notification(admin, structure, services):
    """
    Fonction similaire à celle de l'envoi de notification pour les services en brouillons.
    Placée ici parce que probablement non-reutilisée à l'avenir (et légérement modifiée au passage).
    """
    draft_services = services.filter(structure=structure)[:5]
    draft_structure = draft_services[0].structure if draft_services else None
    cta_draft_services_link = (
        furl(settings.FRONTEND_URL).add(
            path="/auth/connexion",
            args={
                "next": f"/structures/{draft_structure.slug}/services?service-status=DRAFT",
            },
        )
        if draft_structure
        else ""
    )

    context = {
        "user": admin,
        "draft_services": draft_services,
        "cta_draft_services_link": cta_draft_services_link,
        "help_update_services_url": "https://aide.dora.inclusion.gouv.fr/fr/article/actualiser-ses-services-1u0a101/",
    }

    send_mail(
        "Des mises à jour de votre offre de service sur DORA sont nécessaires",
        admin.email,
        mjml2html(render_to_string("notification-services.mjml", context)),
        tags=["service-notification-mednum"],
    )


for structure in target_structures:
    print(f" > Pour la structure: {structure}")
    for admin in structure.admins:
        print(f"  > Notification à: {admin.email}")
        send_service_draft_notification(admin, structure, mednum_draft_services)

print("Traitement terminé")
