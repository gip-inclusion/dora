from django.db import transaction

from dora.structures.models import StructureMember, StructurePutativeMember
from dora.users.models import User

from . import OIDCError

# utilitaires divers et corrections métiers en relation avec Inclusion-Connect / OIDC


def updated_ic_user(user: User, ic_token_email: str) -> tuple[User, bool]:
    # vérification de la cohérence des e-mails lors d'une connexion IC
    # retourne l'utilisateur ciblé et si il doit être mis à jour ou pas

    if ic_token_email != user.email:
        # l'e-mail fourni dans le token JWT IC ne correspond pas à celui de l'utilisateur DORA
        # ayant cet identifiant IC

        # => on vérifie si l'utilisateur est membre d'une structure
        # c'est un cas marginal, on se contente de "crasher" proprement
        if StructureMember.objects.filter(user__email=ic_token_email):
            raise OIDCError(
                f"L'utilisateur '{ic_token_email}' est membre d'une ou plusieurs structures et ne peut être supprimé"
            )

        # => on vérifie si des invitations sont en attente sur le nouvel e-mails
        if obsolete_invitations := StructurePutativeMember.objects.filter(
            user__email=ic_token_email
        ):
            # transaction : tout le bloc mis à jour ou rien :
            with transaction.atomic():
                # si il en existe, on les déplace vers l'utilisateur IC existant
                obsolete_invitations.update(user=user)

                # on supprime l'utilisateur actuel après migration
                User.objects.get(email=ic_token_email).delete()

                # on fini par mettre à jour l'ancien e-mail par le nouveau
                user.email = ic_token_email

        # retourne l'utilisateur maj pour être actualisé plus avant (si besoin)
        return user, True

    # sinon, rien à faire on retourne l'utilisateur inchangé
    return user, False
