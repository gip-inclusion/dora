import argparse
import logging
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dora.settings")
django.setup()

# à charger après le setup...
from dora.structures.models import Structure, StructureNationalLabel  # noqa:E402

NATIONAL_LABEL = "siae"
logging.basicConfig(level=logging.INFO)


def read_siae_sirets(file_path):
    """
    Lit les SIRETs depuis un fichier et les retourne un par un.

    :param file_path: Chemin du fichier contenant les SIRETs.
    :return: Générateur de SIRETs.
    """
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line == "siret":
                    continue
                if len(line) != 14 or not line.isdigit():
                    logging.warning(f"SIRET invalide détecté : {line}")
                    continue
                yield line
    except FileNotFoundError:
        logging.error(f"Fichier introuvable : {file_path}")
    except IOError as e:
        logging.error(f"Erreur d'entrée/sortie : {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import des labels SIAE")
    parser.add_argument("file_path", help="Chemin du fichier d'import des SIAE")
    args = parser.parse_args()

    sirets = list(read_siae_sirets(args.file_path))
    structures = Structure.objects.filter(siret__in=sirets)
    label = StructureNationalLabel.objects.get(value=NATIONAL_LABEL)

    for structure in structures:
        structure.national_labels.add(label)
        logging.info(
            f"Label '{NATIONAL_LABEL}' ajouté à la structure avec le SIRET {structure.siret}"
        )

    logging.info(f"Nombre de structures traitées: {len(structures)}")
