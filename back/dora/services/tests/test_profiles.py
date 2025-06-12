import pytest
from django.core.exceptions import ValidationError

from dora.core.test_utils import make_structure
from dora.services.models import ConcernedPublic


@pytest.fixture
def structure():
    return make_structure()


@pytest.fixture
def concerned_public(structure):
    return ConcernedPublic(name="Test", structure=structure)


def test_valid_profile_families(concerned_public):
    concerned_public.profile_families = ["adultes", "jeunes"]
    concerned_public.full_clean()
    concerned_public.save()
    concerned_public.refresh_from_db()
    assert set(concerned_public.profile_families) == {"adultes", "jeunes"}


def test_invalid_profile_families(concerned_public):
    concerned_public.profile_families = ["invalid-profile", "adultes"]
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.full_clean()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)


def test_invalid_profile_families_on_save(concerned_public):
    concerned_public.profile_families = ["invalid-profile", "adultes"]
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.save()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)


def test_empty_profile_families(concerned_public):
    concerned_public.profile_families = []
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.full_clean()
    assert "profile_families" in str(exc_info.value)


def test_all_valid_profiles(concerned_public):
    from data_inclusion.schema.v0 import Profil

    all_profiles = [p.value for p in Profil]
    concerned_public.profile_families = all_profiles
    concerned_public.full_clean()
    concerned_public.save()
    concerned_public.refresh_from_db()
    assert set(concerned_public.profile_families) == set(all_profiles)


def test_mixed_valid_invalid_profiles(concerned_public):
    concerned_public.profile_families = [
        "adultes",
        "invalid-profile",
        "jeunes",
        "another-invalid",
    ]
    with pytest.raises(ValidationError) as exc_info:
        concerned_public.full_clean()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)
