"""Tests des transformations appliquées par la migration 0006."""

import importlib

import pytest

migration = importlib.import_module(
    "dora.services.migrations.0006_migrate_mobilisation_data"
)
compute_mobilisation_fields = migration.compute_mobilisation_fields


def compute(**kwargs):
    return compute_mobilisation_fields(
        beneficiary_modes=kwargs.get("beneficiary_modes", []),
        coach_modes=kwargs.get("coach_modes", []),
        coach_link=kwargs.get("coach_link", ""),
        beneficiary_link=kwargs.get("beneficiary_link", ""),
        coach_other=kwargs.get("coach_other", ""),
        beneficiary_other=kwargs.get("beneficiary_other", ""),
    )


@pytest.mark.no_django_db
class TestMobilisablePar:
    def test_coach_modes_only(self):
        assert compute(coach_modes=["telephoner"])["mobilisable_par"] == [
            "professionnels"
        ]

    def test_beneficiary_modes_only(self):
        assert compute(beneficiary_modes=["telephoner"])["mobilisable_par"] == [
            "usagers"
        ]

    def test_both(self):
        result = compute(
            coach_modes=["telephoner"], beneficiary_modes=["envoyer-un-mail"]
        )
        assert result["mobilisable_par"] == ["usagers", "professionnels"]

    def test_professionnel_excludes_usagers(self):
        # « Se faire orienter par un professionnel » : le service n'est pas
        # mobilisable directement par les usagers
        result = compute(
            coach_modes=["telephoner"],
            beneficiary_modes=["professionnel", "envoyer-un-mail"],
        )
        assert result["mobilisable_par"] == ["professionnels"]

    def test_professionnel_alone(self):
        result = compute(beneficiary_modes=["professionnel"])
        assert result["mobilisable_par"] == ["professionnels"]
        assert result["modes_mobilisation"] == []

    def test_no_mode_at_all(self):
        assert compute()["mobilisable_par"] == []


@pytest.mark.no_django_db
class TestModesMobilisation:
    def test_fiche_de_prescription_is_merged_with_email(self):
        result = compute(
            coach_modes=[
                "envoyer-un-mail",
                "envoyer-un-mail-avec-une-fiche-de-prescription",
            ]
        )
        assert result["modes_mobilisation"] == ["envoyer-un-courriel"]

    def test_modes_are_deduplicated_across_publics(self):
        result = compute(coach_modes=["telephoner"], beneficiary_modes=["telephoner"])
        assert result["modes_mobilisation"] == ["telephoner"]

    def test_beneficiary_modes_are_kept_when_professionnel_is_present(self):
        result = compute(beneficiary_modes=["professionnel", "se-presenter"])
        assert result["modes_mobilisation"] == ["se-presenter"]

    def test_formulaire_dora_is_kept(self):
        result = compute(coach_modes=["formulaire-dora"])
        assert result["modes_mobilisation"] == ["formulaire-dora"]

    def test_autre_produces_no_mode(self):
        result = compute(coach_modes=["autre"], coach_other="Passer par le CCAS")
        assert result["modes_mobilisation"] == []
        assert result["mobilisation_precisions"] == "Passer par le CCAS"

    def test_canonical_order(self):
        result = compute(
            coach_modes=["formulaire-dora", "telephoner", "envoyer-un-mail"]
        )
        assert result["modes_mobilisation"] == [
            "envoyer-un-courriel",
            "telephoner",
            "formulaire-dora",
        ]


@pytest.mark.no_django_db
class TestLienMobilisation:
    def test_coach_link_wins(self):
        result = compute(
            coach_modes=["completer-le-formulaire-dadhesion"],
            beneficiary_modes=["completer-le-formulaire-dadhesion"],
            coach_link="https://coach.example.com",
            beneficiary_link="https://beneficiaire.example.com",
        )
        assert result["lien_mobilisation"] == "https://coach.example.com"
        assert result["modes_mobilisation"] == ["utiliser-lien-mobilisation"]

    def test_beneficiary_link_used_as_fallback(self):
        result = compute(
            beneficiary_modes=["completer-le-formulaire-dadhesion"],
            beneficiary_link="https://beneficiaire.example.com",
        )
        assert result["lien_mobilisation"] == "https://beneficiaire.example.com"
        assert result["modes_mobilisation"] == ["utiliser-lien-mobilisation"]

    def test_mode_dropped_without_any_link(self):
        result = compute(coach_modes=["completer-le-formulaire-dadhesion"])
        assert result["lien_mobilisation"] == ""
        assert result["modes_mobilisation"] == []

    def test_orphan_link_is_kept_without_mode(self):
        result = compute(
            coach_modes=["telephoner"], coach_link="https://coach.example.com"
        )
        assert result["lien_mobilisation"] == "https://coach.example.com"
        assert result["modes_mobilisation"] == ["telephoner"]

    def test_overwritten_beneficiary_link_goes_to_precisions(self):
        result = compute(
            coach_link="https://coach.example.com",
            beneficiary_link="https://beneficiaire.example.com",
        )
        assert result["lien_mobilisation"] == "https://coach.example.com"
        assert result["mobilisation_precisions"] == (
            "Lien de mobilisation pour les usagers : https://beneficiaire.example.com"
        )

    def test_overwritten_beneficiary_link_is_appended_to_existing_precisions(self):
        result = compute(
            coach_link="https://coach.example.com",
            beneficiary_link="https://beneficiaire.example.com",
            coach_other="Uniquement le mardi",
        )
        assert result["mobilisation_precisions"] == (
            "Uniquement le mardi\n\n"
            "Lien de mobilisation pour les usagers : https://beneficiaire.example.com"
        )

    def test_identical_links_produce_no_precisions(self):
        result = compute(
            coach_link="https://example.com",
            beneficiary_link="https://example.com",
        )
        assert result["lien_mobilisation"] == "https://example.com"
        assert result["mobilisation_precisions"] == ""

    def test_beneficiary_link_alone_produces_no_precisions(self):
        result = compute(beneficiary_link="https://beneficiaire.example.com")
        assert result["lien_mobilisation"] == "https://beneficiaire.example.com"
        assert result["mobilisation_precisions"] == ""


@pytest.mark.no_django_db
class TestMobilisationPrecisions:
    def test_coach_only(self):
        result = compute(coach_other="Uniquement le mardi")
        assert result["mobilisation_precisions"] == "Uniquement le mardi"

    def test_beneficiary_only(self):
        result = compute(beneficiary_other="Sur rendez-vous")
        assert result["mobilisation_precisions"] == "Sur rendez-vous"

    def test_identical_texts_are_not_duplicated(self):
        result = compute(
            coach_other="Sur rendez-vous", beneficiary_other="Sur rendez-vous"
        )
        assert result["mobilisation_precisions"] == "Sur rendez-vous"

    def test_different_texts_are_concatenated_coach_first(self):
        result = compute(
            coach_other="Uniquement le mardi", beneficiary_other="Sur rendez-vous"
        )
        assert (
            result["mobilisation_precisions"]
            == "Uniquement le mardi\n\nSur rendez-vous"
        )

    def test_whitespace_only_is_ignored(self):
        result = compute(coach_other="   ", beneficiary_other="Sur rendez-vous")
        assert result["mobilisation_precisions"] == "Sur rendez-vous"


@pytest.mark.no_django_db
def test_empty_service():
    assert compute() == {
        "modes_mobilisation": [],
        "mobilisable_par": [],
        "mobilisation_precisions": "",
        "lien_mobilisation": "",
    }
