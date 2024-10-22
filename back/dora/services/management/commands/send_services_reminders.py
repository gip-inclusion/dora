from collections import defaultdict
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from dora.services.emails import send_service_reminder_email
from dora.services.models import Service, ServiceStatus
from dora.structures.models import StructureMember
from dora.users.models import User


class Command(BaseCommand):
    help = (
        "Notifications pour les brouillons en souffrance ou les services à actualiser"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-n",
            "--dry-run",
            action="store_true",
            help="N'accomplit aucune action, montre juste le nombre de brouillons, d'utilisateurs, et de courriels concernés.",
        )
        parser.add_argument("--limit", type=int)

    def handle(self, *args, **options):
        # if not settings.IS_TESTING and settings.ENVIRONMENT != "production":
        #     return

        dry_run = options["dry_run"]
        limit = options["limit"]

        if dry_run:
            self.stdout.write(self.style.NOTICE("DRY RUN"))
        else:
            self.stdout.write(self.style.WARNING("PRODUCTION RUN"))

        if limit is not None:
            self.stdout.write(self.style.WARNING(f"Limite d'envoi à {limit} courriels"))

        self.stdout.write(
            f"Vérification des brouillons de plus de {settings.NUM_DAYS_BEFORE_DRAFT_SERVICE_NOTIFICATION} jours…"
        )
        expired_drafts = Service.objects.filter(
            status=ServiceStatus.DRAFT,
            creation_date__lte=timezone.now()
            - timedelta(days=settings.NUM_DAYS_BEFORE_DRAFT_SERVICE_NOTIFICATION),
        )
        self.stdout.write(f"{expired_drafts.count()} brouillons concernés")

        self.stdout.write(
            f"Vérification des services mis à jour depuis plus de  {settings.NUM_DAYS_BEFORE_ADVISED_SERVICE_UPDATE} jours…"
        )
        obsolete_services = Service.objects.update_advised()

        self.stdout.write(f"{obsolete_services.count()} services concernés")

        users = defaultdict(lambda: defaultdict(set))
        store_users_to_notify(expired_drafts, users, "draft")
        store_users_to_notify(obsolete_services, users, "to_update")

        mails_count = 0
        user_list = (
            list(users.items()) if limit is None else list(users.items())[:limit]
        )
        for user, structures in user_list:
            mails_count += 1

            if not dry_run:
                send_service_reminder_email(
                    user.email,
                    user.get_short_name(),
                    structures["to_update"],
                    structures["draft"],
                )
                user.last_service_reminder_email_sent = timezone.now()
                user.save()

        self.stdout.write(
            f"{mails_count} courriels{' seraient ' if dry_run else ' '}envoyés"
        )


def store_users_to_notify(services, users_to_notify, category):
    for service in services:
        pertinent_users = set()

        # Créateur
        if service.creator:
            pertinent_users.add(service.creator)

        # Dernier éditeur
        if service.last_editor:
            pertinent_users.add(service.last_editor)

        # Tous les éditeurs
        for history_items in service.history_item.exclude(user=None):
            pertinent_users.add(history_items.user)

        # Administrateurs
        for admin in StructureMember.objects.filter(
            structure=service.structure, is_admin=True
        ):
            pertinent_users.add(admin.user)

        # Référents
        if service.contact_email:
            user_in_charge = User.objects.filter(
                is_valid=True, is_active=True, email=service.contact_email
            ).first()
            if user_in_charge:
                pertinent_users.add(user_in_charge)

        for user in pertinent_users:
            if service.structure.is_member(user) and (
                not user.last_service_reminder_email_sent
                or user.last_service_reminder_email_sent
                < timezone.now() - timedelta(days=25)
            ):
                users_to_notify[user][category].add(service.structure)
