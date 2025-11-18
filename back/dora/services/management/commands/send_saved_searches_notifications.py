from datetime import timedelta

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from mjml import mjml2html

from dora.core.commands import BaseCommand
from dora.core.emails import send_mail
from dora.services.models import LocationKind

from ...models import SavedSearch, SavedSearchFrequency


def get_saved_search_notifications_to_send():
    # Notifications toutes les deux semaines
    two_weeks_notifications = SavedSearch.objects.filter(
        frequency=SavedSearchFrequency.TWO_WEEKS,
        last_notification_date__lte=timezone.now() - timedelta(days=14),
    )

    # Notifications mensuelles
    monthly_notifications = SavedSearch.objects.filter(
        frequency=SavedSearchFrequency.MONTHLY,
        last_notification_date__lte=timezone.now() - timedelta(days=30),
    )

    return two_weeks_notifications.union(monthly_notifications)


class Command(BaseCommand):
    help = (
        "Envoi les notifications liées aux recherches sauvegardées par les utilisateurs"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_site = LocationKind.objects.get(value="en-presentiel")
        self.remote = LocationKind.objects.get(value="a-distance")

    def handle(self, *args, **options):
        self.stdout.write("Vérification des notifications de recherches sauvegardées")
        saved_searches = get_saved_search_notifications_to_send()
        tracking_params = (
            "mtm_campaign=MailsTransactionnels&mtm_kwd=AlertesNouveauxServices"
        )
        num_emails_sent = 0
        for saved_search in saved_searches:
            # On garde les contenus qui ont été publiés depuis la dernière notification
            new_services = saved_search.get_recent_services(
                saved_search.last_notification_date
            )

            if new_services:
                # Envoi de l'email
                context = {
                    "search_label": self.compute_search_label(saved_search),
                    "updated_services": new_services,
                    "alert_link": f"{settings.FRONTEND_URL}/mes-alertes/{saved_search.id}",
                    "tracking_params": tracking_params,
                }

                num_emails_sent += 1
                send_mail(
                    "Il y a de nouveaux services correspondant à votre alerte",
                    saved_search.user.email,
                    mjml2html(
                        render_to_string("saved-search-notification.mjml", context)
                    ),
                    from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
                    tags=["saved-search-notification"],
                )

            # Mise à jour de la date de dernière notification
            saved_search.last_notification_date = timezone.now()
            saved_search.save()
        self.stdout.write(f"{num_emails_sent} courriels envoyés")

    def compute_search_label(self, saved_search):
        on_site_only = self.on_site in saved_search.location_kinds.all()
        remote_only = self.remote in saved_search.location_kinds.all()
        location_txt = ""
        if on_site_only:
            location_txt = "en présentiel"
        elif remote_only:
            location_txt = "à distance"
        text = f"Services d’insertion {location_txt}{' ' if location_txt else ''}à proximité de {saved_search.city_label}"
        if saved_search.category:
            text += f', pour la thématique "{saved_search.category.label}"'

        if saved_search.subcategories.exists():
            labels = saved_search.subcategories.values_list("label", flat=True)
            text += f", pour le(s) besoin(s) : {', '.join(labels)}"

        if saved_search.kinds.exists():
            labels = saved_search.kinds.values_list("label", flat=True)
            text += f", pour le(s) type(s) de service : {', '.join(labels)}"

        if saved_search.fees.exists():
            labels = saved_search.fees.values_list("label", flat=True)
            text += f", avec comme frais à charge : {', '.join(labels)}"

        return text
