"""Garde-fou sur l'empreinte de synchronisation figée dans les migrations de recalcul.

Ces migrations recalculent les empreintes de tous les modèles après un changement des champs
synchronisés, pour éviter que leurs copies n'apparaissent d'un coup comme « modèle modifié ».
Elles figent leur propre copie du calcul plutôt que d'importer `update_sync_checksum` — le
code applicatif suit le schéma courant et référencerait, dans les migrations les plus
anciennes, des colonnes qui n'existent pas encore à ce point de l'historique.

Le prix de ce figeage est qu'une copie peut diverger du calcul de l'application, et produire
exactement le faux « modèle modifié » que la migration cherche à éviter. Seule la migration de
recalcul la plus récente doit reproduire le calcul courant : les précédentes reproduisent
l'état de leur époque, corrigé par celles qui suivent. C'est donc elle que ce test vérifie —
il rougira au prochain changement des champs synchronisés, signe qu'une nouvelle migration de
recalcul est nécessaire.
"""

from importlib import import_module

from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.core.test_utils import make_model
from dora.services.utils import update_sync_checksum

latest_recompute_migration = import_module(
    "dora.services.migrations.0013_recompute_sync_checksums"
)


def test_latest_recompute_migration_matches_application_checksum():
    model = make_model(fee_condition=baker.make("ServiceFee"))
    model.categories.set(baker.make("ServiceCategory", _quantity=2))
    model.access_conditions.add(
        baker.make("AccessCondition", structure=model.structure)
    )
    # hors empreinte depuis la bascule d'écriture des publics, contrairement à `publics_di`
    model.publics.add(
        baker.make(
            "Public",
            structure=model.structure,
            corresponding_di_publics=[DiPublic.FAMILLES.value],
        )
    )
    model.publics_di = [DiPublic.FAMILLES.value]

    assert latest_recompute_migration.sync_checksum(model) == update_sync_checksum(
        model
    )
