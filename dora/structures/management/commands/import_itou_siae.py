import csv
import logging
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from typing import Tuple

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from dora.core import utils
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.sirene.models import Establishment
from dora.structures.models import Structure, StructureSource, StructureTypology
from dora.users.models import User

logging.basicConfig()
logger = logging.getLogger()


def hexewkb_str_to_lonlat(geom: str) -> Tuple[float, float]:
    pos = GEOSGeometry(geom)
    return pos.x, pos.y


class Command(BaseCommand):
    """Commande d'import des données SIAE d'ITOU depuis format csv

    Les données ITOU siae sont:
    * soit des données de structures taggées comment étant créées par un utilisateur.
    Leurs sirets sont valides et ces structures sont des structures mères.
    * soit des données de structures qui doivent être considérées comme des antennes.
    Structure mères et antennes partagent le même asp_id.

    Parmi les structures mères, un siret peut être dupliqué (le type change notamment).
    """

    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("--log-level", default="INFO", type=str)
        parser.add_argument("input_path", type=Path)

    def handle(self, *args, **options):
        logger.setLevel(options["log_level"])
        itou_siae_input_path = options["input_path"]

        with itou_siae_input_path.open(newline="") as f:
            data = [row for row in csv.DictReader(f)]

        logger.info(f"{len(data)} lignes en entrée")

        antennes = [d for d in data if d["source"] == "USER_CREATED"]
        structures = [d for d in data if d not in antennes]

        structures_by_siret = {
            k: list(g) for k, g in groupby(structures, lambda d: d["siret"])
        }
        antennes_by_asp_id = {
            k: list(g) for k, g in groupby(antennes, lambda d: d["asp_id"])
        }

        structures_by_import_result = defaultdict(list)

        logger.info(f"{len(structures)} structures mères en entrée")
        logger.info(f"{len(antennes)} antennes en entrée")

        with transaction.atomic():
            bot_user = User.objects.get_dora_bot()
            structure_source = StructureSource.objects.get(value="plateforme-inclusion")

            for siret, data in tqdm(
                structures_by_siret.items(), disable=logger.level < logging.INFO
            ):
                if len(data) > 1:
                    # plusieurs structures mères partagent le même siret
                    # la structure ayant le plus de champs renseignés est utilisée
                    datum_by_number_of_fields_set = {
                        len(list(filter(lambda v: v == "", d.values()))): d
                        for d in data
                    }
                    datum = datum_by_number_of_fields_set[
                        min(datum_by_number_of_fields_set)
                    ]
                else:
                    datum = data[0]

                establishment = Establishment.objects.filter(siret=siret).first()
                if establishment is None:
                    logger.debug(f"{siret} probablement fermé. Ignoré")
                    structures_by_import_result["unknown_siret"].append(datum)
                    # structure probablement fermée
                    continue

                structure = Structure.objects.filter(siret=establishment.siret).first()
                if structure is not None:
                    logger.debug(f"{siret} déjà référencé. Ignoré")
                    structures_by_import_result["known_structure"].append(datum)
                    structure.fill_contact(
                        email=datum["email"],
                        phone=utils.normalize_phone_number(datum["phone"]),
                        url=datum["website"],
                    )
                    # structure déjà référencée
                    continue

                # nouvelle structure
                structure = Structure.objects.create_from_establishment(establishment)
                # TODO: ajoute une notification de modération ?
                structure.source = structure_source
                structure.creator = bot_user
                structure.last_editor = bot_user
                structure.name = datum["name"]
                structure.email = datum["email"]
                structure.phone = utils.normalize_phone_number(datum["phone"])
                structure.url = datum["website"]
                structure.short_desc, structure.full_desc = utils.normalize_description(
                    datum["description"], limit=Structure.short_desc.field.max_length
                )
                if datum["coords"] != "":
                    structure.longitude, structure.latitude = hexewkb_str_to_lonlat(
                        datum["coords"]
                    )
                    if datum["geocoding_score"] != "":
                        structure.geocoding_score = float(datum["geocoding_score"])
                else:
                    structure.longitude, structure.latitude = (
                        establishment.longitude,
                        establishment.latitude,
                    )
                structure.typology = StructureTypology.objects.get(value=datum["kind"])
                structure.save()
                send_moderation_notification(
                    structure,
                    bot_user,
                    "Structure créée à partir d'un import ITOU",
                    ModerationStatus.VALIDATED,
                )
                # écriture "manuelle" de la date de modif pour contourner la réécriture
                # automatique par django (dû à `auto_now=``)
                if datum["updated_at"] != "":
                    Structure.objects.filter(id=structure.id).update(
                        modification_date=datum["updated_at"]
                    )

                logger.debug(f"{siret} nouvellement référencé")
                structures_by_import_result["new_structure"].append(datum)

                # antennes associées
                if "asp_id" in datum and datum["asp_id"] in antennes_by_asp_id:
                    for antenne_datum in antennes_by_asp_id[datum["asp_id"]]:
                        antenne = Structure.objects.create(
                            parent=structure,
                            name=antenne_datum["name"],
                            source=structure.source,
                            creator=structure.creator,
                            last_editor=structure.last_editor,
                            address1=antenne_datum["address_line_1"],
                            address2=antenne_datum["address_line_2"],
                            postal_code=antenne_datum["post_code"],
                            city=antenne_datum["city"],
                            email=antenne_datum["email"],
                            phone=utils.normalize_phone_number(antenne_datum["phone"]),
                            url=antenne_datum["website"],
                            typology=StructureTypology.objects.get(value=datum["kind"]),
                        )

                        (
                            antenne.short_desc,
                            antenne.full_desc,
                        ) = utils.normalize_description(
                            datum["description"],
                            limit=Structure.short_desc.field.max_length,
                        )

                        if antenne_datum["coords"] != "":
                            (
                                antenne.longitude,
                                antenne.latitude,
                            ) = hexewkb_str_to_lonlat(antenne_datum["coords"])

                            if datum["geocoding_score"] != "":
                                structure.geocoding_score = float(
                                    datum["geocoding_score"]
                                )
                        else:
                            structure.longitude, structure.latitude = (
                                establishment.longitude,
                                establishment.latitude,
                            )

                        antenne.save()
                        send_moderation_notification(
                            antenne,
                            bot_user,
                            "Structure créée à partir d'un import ITOU",
                            ModerationStatus.VALIDATED,
                        )

                        # écriture "manuelle" de la date de modif pour contourner la réécriture
                        # automatique par django (dû à `auto_now=``)
                        if antenne_datum["updated_at"] != "":
                            Structure.objects.filter(id=antenne.id).update(
                                modification_date=antenne_datum["updated_at"]
                            )

                        logger.debug(
                            f"{antenne_datum['siret']} nouvellement référencé comme "
                            f"antenne de {siret}"
                        )
                        structures_by_import_result["new_structure"].append(
                            antenne_datum
                        )

            logger.info(
                f"{len(structures_by_import_result['new_structure'])} "
                "nouvelles structures"
            )
            logger.info(
                f"{len(structures_by_import_result['known_structure'])} "
                "sirets déjà référencés"
            )
            logger.info(
                f"{len(structures_by_import_result['unknown_siret'])} "
                "entrées non identifiables :"
            )
            for d in structures_by_import_result["unknown_siret"]:
                logger.info(
                    f"https://annuaire-entreprises.data.gouv.fr/etablissement/{d['siret']}"
                )
