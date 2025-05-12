from logging import getLogger

import requests
from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import (
    OIDCAuthenticationBackend as MozillaOIDCAuthenticationBackend,
)
from rest_framework.authtoken.models import Token

from dora.logs import logger as core_logger

logger = getLogger(__name__)


class OIDCAuthenticationBackend(MozillaOIDCAuthenticationBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # On stocke ces informations pendant la vérification des claims
        self.user_safir: str | None = None
        self.user_siret: str | None = None

    def get_userinfo(self, access_token, id_token, payload):
        # Surcharge de la récupération des informations utilisateur:
        # le décodage JSON du contenu JWT pose problème avec ProConnect
        # qui le retourne en format binaire (content-type: application/jwt)
        # d'où ce petit hack.
        # Inspiré de : https://github.com/numerique-gouv/people/src/backend/core/authentication/backends.py
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

    def authenticate(self, request, **kwargs):
        result = super().authenticate(request, **kwargs)
        # à ce point, il est encore possible d'accéder à la session
        # et d'y stocker des informations complémentaires concernant l'utilisateur
        # ici : SIRET et/ou SAFIR
        if self.request and (self.user_safir or self.user_siret):
            self.request.session["_siret_safir"] = {
                "siret": self.user_siret,
                "safir": self.user_safir,
            }
        return result

    def verify_claims(self, claims):
        # Vérification des claims pour extraire et stocker SIRET et SAFIR
        if "custom" in claims:
            self.user_safir = claims["custom"].get("structureTravail")

        self.user_siret = claims.get("siret")

        return super().verify_claims(claims)

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
        sub = claims.get("sub")

        if not sub:
            raise SuspiciousOperation(
                "Le sujet (`sub`) n'est pas inclu dans les `claims`"
            )

        if user.sub_pc and str(user.sub_pc) != sub:
            raise SuspiciousOperation(
                "Le sub enregistré est différent de celui fourni par ProConnect"
            )

        if not user.sub_pc:
            # utilisateur existant, mais non-enregistré sur ProConnect
            user.sub_pc = sub
            # on considère que si l'utilisateur s'est connecté via ProConnect, son e-mail est valide
            user.is_valid = True
            user.save()

        return user

    def get_user(self, user_id):
        # simplement surchargé pour ajout du token DRF
        # note: DRF devrait être déprécié pour utiliser un autre type d'identification entre front et back.
        if user := super().get_user(user_id):
            core_logger.info(
                "Connexion utilisateur via ProConnect",
                {
                    "legal": True,
                    "userEmail": user.email,
                    "userId": user.pk,
                },
            )
            self.get_or_create_drf_token(user)
            return user
        return None

    def get_or_create_drf_token(self, user):
        # Pour être temporairement compatible, on crée un token d'identification DRF lié au nouvel utilisateur.
        # note: DRF devrait être déprécié pour utiliser un autre type d'identification entre front et back.
        if not user:
            raise SuspiciousOperation(
                "Utilisateur non renseigné pour la création du token DRF"
            )

        token, created = Token.objects.get_or_create(user=user)

        if created:
            logger.info("Initialisation du token DRF pour l'utilisateur %s", user)

        return token
