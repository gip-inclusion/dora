import pytest
from django.core.management import call_command

from dora.structures.models import StructureNationalLabel


@pytest.fixture
def load_labels():
    # nettoyage
    StructureNationalLabel.objects.all().delete()
    # charge les fixtures de données présentes dans le répertoire `fixtures` de l'app dans la base de donnée de test
    call_command(
        "loaddata", "dora/structures/fixtures/01_structure_national_labels.json.gz"
    )
