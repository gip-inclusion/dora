import uuid

import pytest
from django.core.exceptions import SuspiciousOperation
from django.urls import reverse

from dora.core.test_utils import make_user
from dora.oidc.backends import OIDCAuthenticationBackend


@pytest.fixture
def backend():
    return OIDCAuthenticationBackend()


def claims(**kwargs):
    return {"sub": str(uuid.uuid4()), "email": "alan.turing@example.com", **kwargs}


class TestCompleteNameClaims:
    """Complétion des claims d'identité depuis l'`id_token`.

    ProConnect ne renvoie pas forcément les mêmes claims via `/userinfo`
    et via l'`id_token` : seul le contenu de `/userinfo` étant transmis
    à `create_user` / `update_user`, les claims manquants doivent être
    complétés depuis l'`id_token`.
    """

    @pytest.mark.no_django_db
    def test_userinfo_claims_have_priority(self, backend):
        userinfo = backend.complete_name_claims(
            {"given_name": "Alan", "usual_name": "Turing"},
            {"given_name": "Alain", "usual_name": "Touring"},
        )

        assert userinfo["given_name"] == "Alan"
        assert userinfo["usual_name"] == "Turing"

    @pytest.mark.no_django_db
    @pytest.mark.parametrize("missing_value", [None, ""])
    def test_missing_claims_filled_from_id_token(self, backend, missing_value):
        userinfo = {"usual_name": "Turing"}
        if missing_value is not None:
            userinfo["given_name"] = missing_value

        userinfo = backend.complete_name_claims(
            userinfo, {"given_name": "Alan", "usual_name": "Touring"}
        )

        assert userinfo["given_name"] == "Alan"
        assert userinfo["usual_name"] == "Turing"

    @pytest.mark.no_django_db
    def test_no_name_claims_at_all_is_logged(self, backend, mocker):
        # cas des comptes qui restent sans prénom ni nom :
        # il doit être tracé, faute de quoi il est invisible.
        logger = mocker.patch("dora.oidc.backends.core_logger")

        userinfo = backend.complete_name_claims(
            {"sub": "a-sub", "siret": "12345678901234"}, {}
        )

        assert "given_name" not in userinfo
        assert "usual_name" not in userinfo

        logger.warning.assert_called_once()
        message, payload = logger.warning.call_args.args
        assert "Claims d'identité manquants" in message
        assert payload["missingClaims"] == ["given_name", "usual_name"]

        # le compte et l'organisation concernés doivent être identifiables
        assert payload["pcSub"] == "a-sub"
        assert payload["siret"] == "12345678901234"

    @pytest.mark.no_django_db
    def test_claim_names_of_both_sources_are_logged(self, backend, mocker):
        # permet de déterminer si ProConnect fournit les claims d'identité
        # via l'`id_token` quand ils sont absents de `/userinfo`.
        logger = mocker.patch("dora.oidc.backends.core_logger")

        backend.complete_name_claims(
            {"sub": "a-sub", "email": "alan.turing@example.com", "siret": "123"},
            {"sub": "a-sub", "aud": "dora", "acr": "eidas1"},
        )

        payload = logger.warning.call_args.args[1]
        assert payload["userinfoClaims"] == ["email", "siret", "sub"]
        assert payload["idTokenClaims"] == ["acr", "aud", "sub"]

    @pytest.mark.no_django_db
    def test_userinfo_claims_are_logged_before_completion(self, backend, mocker):
        # un claim repris de l'`id_token` ne doit pas apparaître comme fourni
        # par `/userinfo` : c'est précisément la distinction que le log mesure.
        logger = mocker.patch("dora.oidc.backends.core_logger")

        backend.complete_name_claims({"sub": "a-sub"}, {"given_name": "Alan"})

        payload = logger.warning.call_args.args[1]
        assert payload["userinfoClaims"] == ["sub"]
        assert payload["idTokenClaims"] == ["given_name"]
        assert payload["missingClaims"] == ["usual_name"]

    @pytest.mark.no_django_db
    def test_claim_values_are_not_logged(self, backend, mocker):
        # seuls les noms des claims sont tracés : pas de données personnelles
        # supplémentaires dans `ActionLog`.
        logger = mocker.patch("dora.oidc.backends.core_logger")

        backend.complete_name_claims(
            {"sub": "a-sub", "siret": "123"}, {"given_name": "Alan"}
        )

        payload = logger.warning.call_args.args[1]
        assert "123" not in str(payload["userinfoClaims"])
        assert "Alan" not in str(payload["idTokenClaims"])

    @pytest.mark.no_django_db
    def test_complete_claims_are_not_logged(self, backend, mocker):
        logger = mocker.patch("dora.oidc.backends.core_logger")

        backend.complete_name_claims({"given_name": "Alan", "usual_name": "Turing"}, {})

        logger.warning.assert_not_called()

    @pytest.mark.no_django_db
    def test_missing_id_token_payload(self, backend):
        # l'`id_token` décodé est toujours fourni par `mozilla-django-oidc`,
        # mais on ne veut pas d'une exception si ce n'est pas le cas.
        assert backend.complete_name_claims({"given_name": "Alan"}, None) == {
            "given_name": "Alan"
        }


class TestCreateUser:
    def test_names_from_claims(self, backend):
        user = backend.create_user(claims(given_name="Alan", usual_name="Turing"))

        assert user.first_name == "Alan"
        assert user.last_name == "Turing"
        assert user.is_valid

    @pytest.mark.parametrize("name_claims", [{}, {"given_name": "", "usual_name": ""}])
    def test_no_placeholder_when_claims_are_missing(self, backend, name_claims):
        # une valeur de remplissage serait transmise telle quelle aux consommateurs
        # des données utilisateur (cf. `nexus_full_sync`, qui filtre sur `""`).
        user = backend.create_user(claims(**name_claims))

        assert user.first_name == ""
        assert user.last_name == ""

    def test_email_is_mandatory(self, backend):
        with pytest.raises(SuspiciousOperation):
            backend.create_user({"sub": str(uuid.uuid4())})

    def test_sub_is_mandatory(self, backend):
        with pytest.raises(SuspiciousOperation):
            backend.create_user({"email": "alan.turing@example.com"})


class TestUpdateUser:
    @pytest.fixture(autouse=True)
    def production_environment(self, settings):
        # les prénom et nom ne sont mis à jour qu'en production
        # (cf. `update_user`)
        settings.ENVIRONMENT = "production"

    def test_names_are_updated_at_each_login(self, backend):
        user = make_user(sub_pc=uuid.uuid4(), first_name="Alain", last_name="Touring")

        backend.update_user(
            user,
            claims(sub=str(user.sub_pc), given_name="Alan", usual_name="Turing"),
        )

        user.refresh_from_db()
        assert user.first_name == "Alan"
        assert user.last_name == "Turing"

    def test_empty_names_are_filled(self, backend):
        user = make_user(sub_pc=uuid.uuid4(), first_name="", last_name="")

        backend.update_user(
            user,
            claims(sub=str(user.sub_pc), given_name="Alan", usual_name="Turing"),
        )

        user.refresh_from_db()
        assert user.first_name == "Alan"
        assert user.last_name == "Turing"

    @pytest.mark.parametrize("name_claims", [{}, {"given_name": "", "usual_name": ""}])
    def test_existing_names_are_kept_when_claims_are_missing(
        self, backend, name_claims
    ):
        user = make_user(sub_pc=uuid.uuid4(), first_name="Alain", last_name="Touring")

        backend.update_user(user, claims(sub=str(user.sub_pc), **name_claims))

        user.refresh_from_db()
        assert user.first_name == "Alain"
        assert user.last_name == "Touring"

    def test_names_are_not_updated_outside_production(self, backend, settings):
        settings.ENVIRONMENT = "local"

        user = make_user(sub_pc=uuid.uuid4(), first_name="Alain", last_name="Touring")

        backend.update_user(
            user,
            claims(sub=str(user.sub_pc), given_name="Alan", usual_name="Turing"),
        )

        user.refresh_from_db()
        assert user.first_name == "Alain"
        assert user.last_name == "Touring"

    def test_sub_is_stored_for_an_existing_user(self, backend):
        user = make_user(sub_pc=None, is_valid=False)
        sub = str(uuid.uuid4())

        backend.update_user(user, claims(sub=sub, given_name="Alan"))

        user.refresh_from_db()
        assert str(user.sub_pc) == sub
        assert user.is_valid

    def test_different_sub_with_same_email_is_accepted(self, backend):
        user = make_user(sub_pc=uuid.uuid4())
        new_sub = str(uuid.uuid4())

        backend.update_user(user, claims(sub=new_sub, email=user.email))

        user.refresh_from_db()
        assert str(user.sub_pc) == new_sub

    def test_different_sub_and_email_is_suspicious(self, backend):
        user = make_user(sub_pc=uuid.uuid4())

        with pytest.raises(SuspiciousOperation):
            backend.update_user(
                user, claims(sub=str(uuid.uuid4()), email="ada.lovelace@example.com")
            )


class TestFullCallback:
    """Vérification du chemin complet : claims ProConnect -> compte DORA."""

    def test_names_from_id_token_only(self, client, mocker, settings):
        settings.ENVIRONMENT = "production"
        # ProConnect peut ne pas exposer les claims d'identité via `/userinfo`
        # alors qu'ils sont présents dans l'`id_token`.
        user = make_user(sub_pc=uuid.uuid4(), first_name="", last_name="")
        backend = "dora.oidc.backends.OIDCAuthenticationBackend"

        mocker.patch(f"{backend}.get_token", return_value={})

        # l'`id_token` (vérifié par `mozilla-django-oidc`) porte les claims d'identité
        mocker.patch(
            f"{backend}.verify_token",
            return_value={
                "sub": str(user.sub_pc),
                "email": user.email,
                "given_name": "Alan",
                "usual_name": "Turing",
            },
        )

        # ... mais la réponse de `/userinfo` ne les contient pas
        userinfo_response = mocker.Mock()
        userinfo_response.json.return_value = {
            "sub": str(user.sub_pc),
            "email": user.email,
        }
        mocker.patch("dora.oidc.backends.requests.get", return_value=userinfo_response)

        session = client.session
        session["oidc_states"] = {"a-state": {"nonce": None, "code_verifier": None}}
        session.save()

        client.get(
            reverse("oidc_authentication_callback"),
            {"code": "a-code", "state": "a-state"},
        )

        user.refresh_from_db()
        assert user.first_name == "Alan"
        assert user.last_name == "Turing"
