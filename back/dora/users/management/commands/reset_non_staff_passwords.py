from dora.core.commands import BaseCommand
from dora.users.models import User


class Command(BaseCommand):
    help = "Rend inutilisables les mots de passe des utilisateurs non-staff"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            default=False,
            help="effectue les modifications demandées (pour de vrai)",
        )

    def handle(self, *args, **options):
        users = list(
            User.objects.filter(is_staff=False).exclude(password__startswith="!")
        )

        self.stdout.write(f"{len(users)} comptes à normaliser")

        if not options["wet_run"]:
            self.stdout.write(self.style.NOTICE("Mode 'dry-run' : rien n'est modifié"))
            return

        for user in users:
            user.set_unusable_password()

        User.objects.bulk_update(users, ["password"], batch_size=1000)

        self.stdout.write(self.style.SUCCESS("Normalisation effectuée"))
