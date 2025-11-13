import csv
from datetime import datetime
from typing import Any, Dict

from django.core.management.base import BaseCommand

from dora.services.models import Service


class Command(BaseCommand):
    help = (
        "Exporte les données des services vers un fichier CSV. "
        "Permet de filtrer par sous-catégories spécifiques ou par sous-catégories se terminant par '--autre'."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--subcategories",
            nargs="+",
            type=str,
            help="Une ou plusieurs sous-catégories (values) à filtrer",
        )
        parser.add_argument(
            "--autre",
            action="store_true",
            help="Sélectionne les services dont la sous-catégorie se termine par '--autre'",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="Chemin du fichier CSV de sortie (par défaut: généré automatiquement)",
        )

    def get_service_data(self, service: Service) -> Dict[str, Any]:
        """
        Génère un dictionnaire avec les données du service.

        Args:
            service: Instance du modèle Service

        Returns:
            Dictionnaire contenant les données du service
        """

        return {
            "id": service.id,
            "slug": service.slug,
            "nom": service.name.strip(),
            "description_courte": service.short_desc.strip(),
            "description_longue": service.full_desc.strip(),
        }

    def handle(self, *args, **options):
        subcategories = options.get("subcategories")
        autre = options.get("autre")

        # Validation des arguments
        if not subcategories and not autre:
            self.stdout.write(
                self.style.ERROR(
                    "Erreur: Vous devez spécifier au moins --subcategories ou --autre"
                )
            )
            return

        # Construction de la requête
        filters = []
        messages = []

        if subcategories:
            filters.append(
                Service.objects.filter(subcategories__value__in=subcategories)
            )
            messages.append(f"sous-catégories: {', '.join(subcategories)}")

        if autre:
            filters.append(
                Service.objects.filter(subcategories__value__endswith="--autre")
            )
            messages.append("sous-catégories se terminant par '--autre'")

        if len(filters) == 1:
            services = filters[0].distinct()
            self.stdout.write(f"Recherche des services avec {messages[0]}...\n")
        else:
            # Combinaison: sous-catégories spécifiques OU se terminant par --autre
            services = filters[0].distinct() | filters[1].distinct()
            self.stdout.write(
                f"Recherche des services avec {', ou '.join(messages)}...\n"
            )

        # Rassemblement des données
        service_data_list = []
        for service in services:
            service_data = self.get_service_data(service)
            service_data_list.append(service_data)

        self.stdout.write(
            self.style.SUCCESS(
                f"Nombre de services trouvés: {len(service_data_list)}\n"
            )
        )

        # Affichage des résultats
        if service_data_list:
            self.stdout.write("=== Résumé ===\n")
            for item in service_data_list[:5]:  # Afficher les 5 premiers
                self.stdout.write(f"- Service: {item['nom']}")

            if len(service_data_list) > 5:
                self.stdout.write(
                    f"\n... et {len(service_data_list) - 5} autres services"
                )

        # Génération du fichier CSV de sortie
        if options["output"]:
            output_file = options["output"]
        else:
            output_file = f"service_data_for_classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
            fieldnames = [
                "id",
                "slug",
                "nom",
                "description_courte",
                "description_longue",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(service_data_list)

        self.stdout.write(
            self.style.SUCCESS(f"\nDonnées sauvegardées dans: {output_file}")
        )
