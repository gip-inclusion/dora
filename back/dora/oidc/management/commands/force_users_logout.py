from django.core.management.base import BaseCommand
from django.db.models import Q
from rest_framework.authtoken.models import Token

from dora.oidc.models import UserSession

"""
`force_users_logout` :
    Déconnecte (de force) les utilisateurs du backend Django en supprimant
    les tokens DRF qui leur sont associés.
    Quelques exceptions pour la déconnexion "en masse" :
        - les utilisateurs ayant une adresse en `@beta.gouv.fr`,
        - les utilisateurs `staff`,
        - les tokens d'API pour Data·Inclusion.
    Le paramètre `--force` permet de passer outre ces restrictions.
    Le paramètre `--target` permet de cibler des utilisateurs par une liste d'adresses.
    Le paramètre `--domain` permet de déconnecter les utilisateurs d'une domaine donné.
    e-mails séparés par des virgules.
"""

API_TOKEN_EMAILS = ["data.inclusion@beta.gouv.fr"]


class Command(BaseCommand):
    help = "Force la déconnexion des utilisateurs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="""Effectue la déconnexion "pour de vrai" (mode 'dry-run' par défaut)""",
        )
        parser.add_argument(
            "-n",
            "--number",
            type=int,
            default=100,
            help="Nombre d'utilisateur à déconnecter",
        )
        parser.add_argument(
            "-o",
            "--old",
            action="store_true",
            help="Force la déconnexion des anciens utilisateurs IC",
        )
        parser.add_argument(
            "-t",
            "--targets",
            type=str,
            help="Liste d'utilisateurs à déconnecter (e-mails séparés par des virgules)",
        )
        parser.add_argument(
            "-d",
            "--domain",
            type=str,
            help="Domaine d'utilisateurs à déconnecter (par ex.: '@francetravail.fr')",
        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="""Force la déconnexion, sans restrictions""",
        )

    def handle(self, *args, **options):
        wet_run = options["wet_run"]
        number = options["number"]
        targets = options["targets"]
        domain = options["domain"]
        force = options["force"]

        candidates = Token.objects.select_related("user").order_by("created")

        self.stdout.write(self.style.NOTICE("Déconnexion des utilisateurs"))

        if not force:
            self.stdout.write(
                " > déconnexion (hors adresses @beta.gouv.fr, staff et API D·I)"
            )
            candidates = candidates.exclude(
                Q(user__email__endswith="@beta.gouv.fr")
                | Q(user__is_staff=True)
                | Q(user__email__in=API_TOKEN_EMAILS)
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    " > déconnexion forcée des comptes PC (pas de restrictions)"
                )
            )

        if targets:
            target_emails = targets.split(",")
            candidates = candidates.filter(user__email__in=target_emails)
            self.stdout.write(" > déconnexion d'une liste d'utilisateurs :")
            for email in target_emails:
                self.stdout.write(f"  - {email}")

        if domain:
            if not domain.startswith("@"):
                self.stdout.write(
                    self.style.ERROR(
                        f"Le domaine `{domain}` est incorrect (doit commencer par un '@')"
                    )
                )
            candidates = candidates.filter(user__email__endswith=domain)
            self.stdout.write(f" > déconnexion des utilisateurs du domaine '{domain}'")

        # Dernière opération à faire sur un queryset (slice)
        candidates = candidates[:number]

        self.stdout.write(f" > {number} utilisateur(s) max. à déconnecter")
        self.stdout.write(f" > nombre d'utilisateurs concernés : {candidates.count()}")

        if not wet_run:
            self.stdout.write(
                self.style.WARNING(" > DRY_RUN : aucune action supplémentaire")
            )
            return

        # les querysets slicés ne sont plus modifiables, mais :
        to_delete = Token.objects.filter(
            pk__in=candidates.values_list("pk")
        ).select_related("user")
        # liste des utilisateurs pouvant avoir une session Django enregistrée
        user_ids = candidates.values_list("user_id")

        # si des sessions Django sont associées à ces tokens / utilisateurs,
        # elles sont détruites.
        # On fait d'une pierre deux coups, en déconnectant proprement et en évitant
        # certains effets de bords pour la déconnexion de comptes ProConnect.
        user_sessions = UserSession.objects.filter(user_id__in=user_ids).select_related(
            "session"
        )
        nb_sessions = user_sessions.count()
        for user_session in user_sessions:
            user_session.session.delete()

        self.stdout.write(
            self.style.NOTICE(f" > {nb_sessions} sessions(s) supprimée(s)")
        )

        # destructions des tokens DRF
        nb_tokens, _ = to_delete.delete()

        self.stdout.write(self.style.NOTICE(f" > {nb_tokens} token(s) supprimé(s)"))
