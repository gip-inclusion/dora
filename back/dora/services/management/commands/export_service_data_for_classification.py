import csv
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict

from django.core.management.base import BaseCommand
from django.db.models import Count, F, Q

from dora.services.models import Service, ServiceCategory


class Command(BaseCommand):
    generalist_category = "accompagnement-social-et-professionnel-personnalise--parcours-d-insertion-socioprofessionnel"

    help = (
        "Exporte les données des services vers un fichier CSV. "
        "Filtre automatiquement les services ayant uniquement des sous-catégories se terminant par '--autre' "
        f"et/ou la sous-catégorie '{generalist_category}'."
    )

    def add_arguments(self, parser):
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
        categories_dict = defaultdict(list)

        for subcat in service.subcategories.all().order_by("value"):
            category_value = (
                subcat.value.split("--")[0] if "--" in subcat.value else None
            )

            if category_value:
                try:
                    category = ServiceCategory.objects.get(value=category_value)
                    category_label = category.label
                except ServiceCategory.DoesNotExist:
                    category_label = category_value
                categories_dict[category_label].append(subcat.label)

        formatted_subcats = []
        for category_label in sorted(categories_dict.keys()):
            subcats = categories_dict[category_label]
            for subcat_label in subcats:
                formatted_subcats.append(f"{category_label} > {subcat_label}")

        joined_formatted_subcats = "\n".join(formatted_subcats)

        return {
            "id": service.id,
            "slug": service.slug,
            "nom": service.name.strip(),
            "description_courte": service.short_desc.strip(),
            "description_longue": service.full_desc.strip(),
            "thematiques_existantes": joined_formatted_subcats,
        }

    def handle(self, *args, **options):
        # Filtre pour les services ayant uniquement des sous-catégories se terminant par "--autre"
        # ou la sous-catégorie généraliste

        self.stdout.write(
            "Recherche des services ayant uniquement des sous-catégories se terminant par '--autre' "
            f"et/ou la sous-catégorie '{self.generalist_category}'...\n"
        )

        # Filtrer les services qui ont UNIQUEMENT des sous-catégories généralistes
        # On annote chaque service avec :
        # - Le nombre total de sous-catégories
        # - Le nombre de sous-catégories généralistes (se terminant par --autre ou égales à generalist_category)
        # On ne garde que ceux où ces deux nombres sont égaux
        services = (
            Service.objects.annotate(
                total_subcats=Count("subcategories", distinct=True),
                generalist_subcats=Count(
                    "subcategories",
                    filter=Q(subcategories__value__endswith="--autre")
                    | Q(subcategories__value=self.generalist_category),
                    distinct=True,
                ),
            )
            .filter(total_subcats__gt=0)  # Au moins une sous-catégorie
            .filter(
                total_subcats=F("generalist_subcats")
            )  # Toutes les sous-catégories sont généralistes
            .distinct()
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
                "thematiques_existantes",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(service_data_list)

        self.stdout.write(
            self.style.SUCCESS(f"\nDonnées sauvegardées dans: {output_file}")
        )
