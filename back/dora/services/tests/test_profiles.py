import pytest
from data_inclusion.schema.v1.publics import Public as DiPublic
from django.core.exceptions import ValidationError

from dora.core.test_utils import make_structure
from dora.services.models import Public


@pytest.fixture
def structure():
    return make_structure()


@pytest.fixture
def concerned_public(structure):
    return Public(name="Test", structure=structure)


def test_valid_corresponding_di_publics(concerned_public):
    concerned_public.corresponding_di_publics = [DiPublic.FAMILLES, DiPublic.JEUNES]
    concerned_public.full_clean()
    concerned_public.save()
    concerned_public.refresh_from_db()
    assert set(concerned_public.corresponding_di_publics) == {
        DiPublic.FAMILLES,
        DiPublic.JEUNES,
    }


def test_invalid_corresponding_di_publics(concerned_public):
    concerned_public.corresponding_di_publics = ["invalid-profile", DiPublic.FAMILLES]
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.full_clean()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)


def test_invalid_corresponding_di_publics_on_save(concerned_public):
    concerned_public.corresponding_di_publics = ["invalid-profile", DiPublic.FAMILLES]
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.save()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)


def test_empty_corresponding_di_publics(concerned_public):
    concerned_public.corresponding_di_publics = []
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.full_clean()
    assert "corresponding_di_publics" in str(exc_info.value)


def test_all_valid_profiles(concerned_public):
    all_profiles = [p.value for p in DiPublic]
    concerned_public.corresponding_di_publics = all_profiles
    concerned_public.full_clean()
    concerned_public.save()
    concerned_public.refresh_from_db()
    assert set(concerned_public.corresponding_di_publics) == set(all_profiles)


def test_mixed_valid_invalid_profiles(concerned_public):
    concerned_public.corresponding_di_publics = [
        DiPublic.FAMILLES,
        "invalid-profile",
        DiPublic.JEUNES,
        "another-invalid",
    ]
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.full_clean()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)
