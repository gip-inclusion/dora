from rest_framework import exceptions, permissions

from dora.structures.models import Structure


class StructurePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Personne ne peut supprimer une structure
        if request.method == "DELETE":
            return False

        # Tout le monde peut **voir** les structures
        elif request.method in permissions.SAFE_METHODS:
            return True

        # Les utilisateurs connectés peuvent potentiellement
        # créer ou modifier des structures
        # (`has_object_permission` déterminera par la suite lesquelles)
        else:
            return user and user.is_authenticated

    def has_object_permission(self, request, view, structure: Structure):
        user = request.user

        # Lecture : tout le monde peut voir les structures
        if request.method in permissions.SAFE_METHODS:
            return True

        # Écriture :
        return structure.can_edit_informations(user)


class StructureMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Les utilisateurs non connectés ne peuvent jamais
        # voir les autres utilisateurs
        if not (user and user.is_authenticated):
            return False

        # L'API ne permet pas de créer des `Member` directement
        # (il faut passer par un PutativeMember)
        elif request.method == "POST":
            return False

        # Les utilisateurs connectés peuvent voir ou éditer certains autres utilisateurs
        # (`has_object_permission` determinera par la suite lesquels)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        assert user and user.is_authenticated  # Vérifié par has_permission

        # Les superusers ont tous les droits
        if user.is_staff:
            return True

        # Les administrateurs de structure et les gestionnaires ont tous les droits sur les collaborateurs
        elif obj.structure.is_admin(user) or obj.structure.is_manager(user):
            return True

        # Les collaborateurs d'une structure peuvent **voir** leurs collègues
        elif obj.structure.is_member(user):
            return request.method in permissions.SAFE_METHODS

        # Par défaut, aucun accès aux collaborateurs des autres structures
        else:
            return False


class StructurePutativeMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Les utilisateurs non connectés ne peuvent jamais
        # voir, ni éditer de membres potentiels
        if not (user and user.is_authenticated):
            return False

        # Les utilisateurs connectés peuvent **voir** certains autres utilisateurs
        # (`has_object_permission` determinera par la suite lesquels)
        elif request.method in permissions.SAFE_METHODS:
            return True

        # droit de création
        elif request.method == "POST":
            # Il est nécessaire de préciser la structure
            structure_slug = request.query_params.get("structure")
            if not structure_slug:
                return False
            try:
                structure = Structure.objects.get(slug=structure_slug)
            except Structure.DoesNotExist:
                raise exceptions.NotFound

            # Les superuser peuvent inviter
            if user.is_staff:
                return True
            # Les administrateurs peuvent inviter
            elif structure.is_admin(user):
                return True
            # Les gestionnaires peuvent inviter
            elif structure.is_manager(user):
                return True
            # Les autres catégories d'utilisateur ne peuvent pas inviter
            else:
                return False
        # impossible de modifier un utilisateur potentiel
        # Note: pour annuler une invitation on passe pour l'instant par
        # StructurePutativeMemberViewset.cancel_invite
        # et non pas par un DELETE (ce qui n'est pas forcement une bonne idée)
        else:
            return False
