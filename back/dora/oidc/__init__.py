from logging import getLogger

import requests
from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import (
    OIDCAuthenticationBackend as MozillaOIDCAuthenticationBackend,
)
from rest_framework.authtoken.models import Token

from dora.users.models import User

logger = getLogger(__name__)


class OIDCError(Exception):
    """Exception générique pour les erreurs OIDC"""


class OIDCAuthenticationBackend(MozillaOIDCAuthenticationBackend):
    def get_userinfo(self, access_token, id_token, payload):
        # Surcharge de la récupération des informations utilisateur:
        # le décodage JSON du contenu JWT pose problème avec ProConnect
        # qui le retourne en format binaire (content-type: application/jwt)
        # d'où ce petit hack.
        # Inspiré de : https://github.com/numerique-gouv/people/blob/b637774179d94cecb0ef2454d4762750a6a5e8c0/src/backend/core/authentication/backends.py#L47C1-L47C57
        user_response = requests.get(
            self.OIDC_OP_USER_ENDPOINT,
            headers={"Authorization": "Bearer {0}".format(access_token)},
            verify=self.get_settings("OIDC_VERIFY_SSL", True),
            timeout=self.get_settings("OIDC_TIMEOUT", None),
            proxies=self.get_settings("OIDC_PROXY", None),
        )
        user_response.raise_for_status()

        try:
            # cas où le type du token JWT est `application/json`
            return user_response.json()
        except requests.exceptions.JSONDecodeError:
            # sinon, on présume qu'il s'agit d'un token JWT au format `application/jwt` (+...)
            # comme c'est le cas pour ProConnect.
            return self.verify_token(user_response.text)

    # Pas nécessaire de surcharger `get_or_create_user` puisque sur DORA,
    # les utilisateurs ont un e-mail unique qui leur sert de `username`.

    def create_user(self, claims):
        # on peut à la rigueur se passer de certains élements contenus dans les claims,
        # mais pas de ceux-là :
        email, sub = claims.get("email"), claims.get("sub")
        if not email:
            raise SuspiciousOperation(
                "L'adresse e-mail n'est pas incluse dans les `claims`"
            )

        if not sub:
            raise SuspiciousOperation(
                "Le sujet (`sub`) n'est pas inclus dans les `claims`"
            )

        # L'utilisateur est créé sans mot de passe (aucune connexion à l'admin),
        # et comme venant de ProConnect, on considère l'e-mail vérifié.
        new_user = self.UserModel.objects.create_user(
            email,
            sub_pc=sub,
            first_name=claims.get("given_name", "N/D"),
            last_name=claims.get("usual_name", "N/D"),
            is_valid=True,
        )

        # recupération du code SAFIR :
        # même pour l'instant inutilisé, on pourra par la suite le passer au frontend
        # pour rattachement direct à une agence France Travail
        if custom := claims.get("custom"):
            code_safir = custom.get("structureTravail")  # noqa F481
            # TODO: une fois le code SAFIR récupéré, voir quoi en faire (redirection vers un rattachement)

        # compatibilité :
        # durant la phase de migration vers ProConnect on ne replace *que* le fournisseur d'identité,
        # et on ne touche pas aux mécanismes d'identification entre back et front.
        self.get_or_create_drf_token(new_user)

        return new_user

    def update_user(self, user, claims):
        # L'utilisateur peut déjà étre inscrit à IC, dans ce cas on réutilise la plupart
        # des informations déjà connues

        if not user.sub_pc:
            # utilisateur existant, mais non-enregistré sur ProConnect
            sub = claims.get("sub")
            if not sub:
                raise SuspiciousOperation(
                    "Le sujet (`sub`) n'est pas inclu dans les `claims`"
                )
            user.sub_pc = sub
            user.save()

        return user

    def get_user(self, user_id):
        if user := super().get_user(user_id):
            self.get_or_create_drf_token(user)
            return user
        return None

    def get_or_create_drf_token(self, user_email):
        # Pour être temporairement compatible, on crée un token d'identification DRF lié au nouvel utilisateur.
        if not user_email:
            raise SuspiciousOperation(
                "Utilisateur non renseigné pour la création du token DRF"
            )

        user = User.objects.get(email=user_email)

        token, created = Token.objects.get_or_create(user=user)

        if created:
            logger.info("Initialisation du token DRF pour l'utilisateur %s", user_email)

        return token
