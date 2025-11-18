from dora.core.commands import BaseCommand
from dora.orientations.models import Orientation


class Command(BaseCommand):
    help = "Supprime les pièces-jointes d'une orientation via son identifiant"

    def add_arguments(self, parser):
        parser.add_argument(
            "orientation_id", type=int, help="Identifiant de l'orientation"
        )

    def handle(self, *args, **options):
        orientation_id = options["orientation_id"]
        try:
            orientation = Orientation.objects.get(id=orientation_id)
            results = orientation.delete_attachments()
            if all(results.values()):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Les pièces-jointes de l'orientation #{orientation_id} ont été supprimées avec succès."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Certaines pièces-jointes de l'orientation n'ont pas pu être supprimées :"
                    )
                )
                for path, result in results.items():
                    if not result:
                        self.stdout.write(self.style.WARNING(f" > {path} : KO"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f" > {path} : OK"))

        except Orientation.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"L'orientation avec l'identifiant #{orientation_id} n'existe pas."
                )
            )
