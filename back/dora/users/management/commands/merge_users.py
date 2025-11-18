"""
Cette commande permet de fusionner deux utilisateurs,
référencés "source" et "destination" (`src_user`, `dest_user`).

Sont fusionnées vers l'utilisateurs de destination :
    - les invitations en attente,
    - les appartenances à une structure ou agence FT.

L'utilisateur source est désactivé en fin de procédure et peut éventuellement
être détruit en utilisant l'option `--delete`.
"""

from django.db.utils import IntegrityError

from dora.core.commands import BaseCommand
from dora.structures.models import StructureMember, StructurePutativeMember
from dora.users.models import User


class Command(BaseCommand):
    help = "Fusionne deux utilisateurs DORA (src vers dest)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            default=False,
            help="effectue les modifications demandées (pour de vrai)",
        )
        parser.add_argument(
            "src",
            type=str,
            help="e-mail de l'utilisateur source",
        )
        parser.add_argument(
            "dest",
            type=str,
            help="e-mail de l'utilisateur destination",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            default=False,
            help="supprime *définitivement* l'utilisateur source en fin d'éxecution",
        )

    def handle(self, *args, **options):
        src_email = options["src"]
        dest_email = options["dest"]
        delete = options["delete"]
        wet_run = options["wet_run"]

        if src_email == dest_email:
            self.stdout.write("Les deux utilisateurs sont identiques")
            return

        msg = (
            "Mode 'wet-run' : les modifications seront effectuées"
            if wet_run
            else "Mode 'dry-run' : les modifications ne seront pas effectuées"
        )

        self.stdout.write(self.style.NOTICE(msg))

        self.stdout.write(f"Fusion de '{src_email}' vers '{dest_email}'")

        if delete:
            self.stdout.write(
                self.style.NOTICE(
                    "Suppression de l'utilisateur source en fin d'éxecution"
                )
            )

        try:
            src_user = User.objects.get_by_email(src_email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Utilisateur '{src_email}' introuvable")
            )
            return

        try:
            dest_user = User.objects.get_by_email(dest_email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Utilisateur '{dest_email}' introuvable")
            )
            return

        self.merge_users(src_user, dest_user, delete=delete, wet_run=wet_run)

        self.stdout.write(self.style.SUCCESS("Fusion effectuée"))

    def merge_users(self, src: User, dest: User, delete=False, wet_run=False):
        self._merge_memberships(src, dest, delete=delete, wet_run=wet_run)
        self._merge_invitations(src, dest, delete=delete, wet_run=wet_run)
        if delete:
            self.stdout.write(f"> suppression de l'utilisateur {src.email}")
            if wet_run:
                src.delete()
        else:
            self.stdout.write(f"> désactivation de l'utilisateur {src.email}")
            if wet_run:
                src.is_active = False
                src.save()

    def _merge_memberships(self, src: User, dest: User, delete=False, wet_run=False):
        src_memberships = list(src.membership.all())

        if not src_memberships:
            self.stdout.write(f"> {src.email} n'est membre d'aucune structure")
            return

        self.stdout.write(f"> fusion des appartenances de {src.email} :")

        for src_membership in src_memberships:
            # attention : on remplace les éventuelles appartenances de l'utilisateur
            # de destination par celle de l'utilisateur source si elles existent des deux cotés.
            try:
                self.stdout.write(f" > ajout de {src_membership.structure}")
                if wet_run:
                    new_membership = StructureMember(
                        user=dest,
                        structure_id=src_membership.structure_id,
                        is_admin=src_membership.is_admin,
                    )
                    new_membership.save()
            except IntegrityError:
                self.stdout.write(
                    f"  > {dest.email} est déjà membre de : {src_membership.structure}"
                )

        if delete:
            # la suppression des objets liés permet de supprimer simplement l'utilisateur source
            try:
                self.stdout.write(f" > suppression des appartenances de {src.email}")
                if wet_run:
                    src.memberships.all().delete()
            except Exception as ex:
                self.stdout.write(
                    self.style.ERROR(
                        f"Erreur à la suppression des appartenances : {ex}"
                    )
                )

    def _merge_invitations(self, src: User, dest: User, delete=False, wet_run=False):
        src_invitations = list(src.putative_membership.all())

        if not src_invitations:
            self.stdout.write(f"> {src.email} n'a aucune invitation en attente")
            return

        self.stdout.write(f"> fusion des invitations de {src.email} :")

        for src_invitation in src_invitations:
            # attention : on remplace les éventuelles invitations de l'utilisateur
            # de destination par celle de l'utilisateur source si elles existent des deux cotés.
            try:
                self.stdout.write(f" > ajout de {src_invitation.structure}")
                if wet_run:
                    new_invitation = StructurePutativeMember(
                        user=dest,
                        structure_id=src_invitation.structure_id,
                        is_admin=src_invitation.is_admin,
                        invited_by_admin=src_invitation.invited_by_admin,
                    )
                    new_invitation.save()
            except IntegrityError:
                self.stdout.write(
                    f"  > {src.email} est déjà invité à : {src_invitation.structure}"
                )

        if delete:
            # la suppression des objets liés permet de supprimer simplement l'utilisateur source
            try:
                self.stdout.write(f" > suppression des invitations de {src.email}")
                if wet_run:
                    src.putative_memberships.all().delete()
            except Exception as ex:
                self.stdout.write(
                    self.style.ERROR(f"Erreur à la suppression des invitations : {ex}")
                )
