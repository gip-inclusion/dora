import pytest
from data_inclusion.schema.v1.publics import Public as DiPublic
from django.core.exceptions import ValidationError

from dora.core.test_utils import make_structure
from dora.services.models import Public


@pytest.fixture
def structure():
    return make_structure()


@pytest.fixture
def public(structure):
    return Public(name="Test", structure=structure)


def test_valid_corresponding_di_publics(public):
    public.corresponding_di_publics = [DiPublic.FAMILLES, DiPublic.JEUNES]
    public.full_clean()
    public.save()
    public.refresh_from_db()
    assert set(public.corresponding_di_publics) == {
        DiPublic.FAMILLES,
        DiPublic.JEUNES,
    }


def test_invalid_corresponding_di_publics(public):
    public.corresponding_di_publics = ["invalid-profile", DiPublic.FAMILLES]
    with pytest.raises(ValidationError) as exc_info:
        public.full_clean()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)


def test_invalid_corresponding_di_publics_on_save(public):
    public.corresponding_di_publics = ["invalid-profile", DiPublic.FAMILLES]
    with pytest.raises(ValidationError) as exc_info:
        public.save()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)


def test_empty_corresponding_di_publics(public):
    public.corresponding_di_publics = []
    with pytest.raises(ValidationError) as exc_info:
        public.full_clean()
    assert "corresponding_di_publics" in str(exc_info.value)


def test_all_valid_profiles(public):
    all_profiles = [p.value for p in DiPublic]
    public.corresponding_di_publics = all_profiles
    public.full_clean()
    public.save()
    public.refresh_from_db()
    assert set(public.corresponding_di_publics) == set(all_profiles)


def test_mixed_valid_invalid_profiles(public):
    public.corresponding_di_publics = [
        DiPublic.FAMILLES,
        "invalid-profile",
        DiPublic.JEUNES,
        "another-invalid",
    ]
    with pytest.raises(ValidationError) as exc_info:
        public.full_clean()
    assert "Invalid profile family: invalid-profile" in str(exc_info.value)
