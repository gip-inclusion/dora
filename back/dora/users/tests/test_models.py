from dora.core.test_utils import make_structure, make_user


def test_should_join_structure():
    user = make_user()

    assert user.should_join_structure(
        siret="12345678901234"
    ), "L'utilisateur devrait pouvoir rejoindre la structure"
    assert user.should_join_structure(
        safir="02012",
    ), "L'utilisateur devrait pouvoir rejoindre cette agence FT"


def test_should_not_join_structure():
    user = make_user()
    structure = make_structure(putative_member=user)

    assert not user.should_join_structure(
        siret=structure.siret
    ), "L'utilisateur ne devrait pas pouvoir rejoindre la structure (invité)"

    structure = make_structure(user=user)
    assert not user.should_join_structure(
        siret=structure.siret
    ), "L'utilisateur ne devrait pas pouvoir rejoindre la structure (membre)"


def test_should_not_join_ft_agency():
    user = make_user()
    make_structure(putative_member=user, code_safir_pe="02012")

    assert not user.should_join_structure(
        safir="02012"
    ), "L'utilisateur ne devrait pas pouvoir rejoindre cette agence (invité)"

    make_structure(user=user, code_safir_pe="02013")
    assert not user.should_join_structure(
        safir="02013"
    ), "L'utilisateur ne devrait pas pouvoir rejoindre cette agence (membre)"
