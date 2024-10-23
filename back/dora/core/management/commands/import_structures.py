import csv
from pprint import pformat

from django.core.management.base import BaseCommand
from rest_framework import serializers

from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.validators import validate_phone_number, validate_siret
from dora.services.models import ServiceModel
from dora.services.utils import instantiate_model
from dora.sirene.models import Establishment
from dora.structures.emails import send_invitation_email
from dora.structures.models import (
    Structure,
    StructureMember,
    StructureNationalLabel,
    StructurePutativeMember,
    StructureSource,
)
from dora.users.models import User

##############################################################################
# Script d’import en masse de structure.
# TODO: est-ce que c'est toujours vrai?
# Les administrateurs proposés ne seront ajoutés que s’il n’y a pas déjà
# un administrateur
#
# Format du CSV attendu (entête):
# | nom | siret | siret_parent | courriels_administrateurs | labels | modeles | telephone | courriel_structure


def to_string_array(strings_list):
    clean_str = strings_list.strip()
    if clean_str:
        return [value.strip() for value in clean_str.split(",")]
    return []


class ImportSerializer(serializers.Serializer):
    name = serializers.CharField()
    siret = serializers.CharField(allow_blank=True, validators=[validate_siret])
    parent_siret = serializers.CharField(allow_blank=True, validators=[validate_siret])
    admins = serializers.ListField(child=serializers.EmailField(), allow_empty=True)
    labels = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    models = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    phone = serializers.CharField(allow_blank=True, validators=[validate_phone_number])
    email = serializers.EmailField(allow_blank=True)

    def _clean_siret_or_phone(self, siret_or_phone: str):
        if not siret_or_phone:
            return ""
        return "".join([c for c in siret_or_phone if c.isdigit()])

    def to_internal_value(self, data):
        # nettoyage pré-validation
        data |= {
            "siret": self._clean_siret_or_phone(data["siret"]),
            "phone": self._clean_siret_or_phone(data["phone"]),
            "parent_siret": self._clean_siret_or_phone(data["parent_siret"]),
        }

        return super().to_internal_value(data)

    def validate_siret(self, siret):
        if (
            siret
            and not Structure.objects.filter(siret=siret).exists()
            and not Establishment.objects.filter(siret=siret).exists()
        ):
            raise serializers.ValidationError(
                f"Siret inconnu: https://annuaire-entreprises.data.gouv.fr/etablissement/{siret}"
            )
        return siret

    def validate_parent_siret(self, parent_siret):
        if (
            parent_siret
            and not Structure.objects.filter(siret=parent_siret).exists()
            and not Establishment.objects.filter(siret=parent_siret).exists()
        ):
            raise serializers.ValidationError(
                f"SIRET parent inconnu: https://annuaire-entreprises.data.gouv.fr/etablissement/{parent_siret}"
            )

        if Structure.objects.filter(siret=parent_siret, parent__isnull=False).exists():
            raise serializers.ValidationError(
                f"Le SIRET {parent_siret} est une antenne, il ne peut pas être utilisé comme parent"
            )

        return parent_siret

    def validate(self, data):
        siret = data.get("siret")
        parent_siret = data.get("parent_siret")

        if not siret and not parent_siret:
            raise serializers.ValidationError("`siret` ou `parent_siret` sont requis")

        return super().validate(data)

    def validate_labels(self, label_slugs):
        labels = []
        for label in label_slugs:
            try:
                label_obj = StructureNationalLabel.objects.get(value=label)
                labels.append(label_obj)
            except StructureNationalLabel.DoesNotExist:
                raise serializers.ValidationError(f"Label inconnu {label}")
        return labels

    def validate_models(self, model_slugs):
        models = []
        for slug in model_slugs:
            try:
                model = ServiceModel.objects.get(slug=slug)
                models.append(model)
            except ServiceModel.DoesNotExist:
                raise serializers.ValidationError(f"Modèle inconnu {slug}")
        return models


class Command(BaseCommand):
    help = "Importe une liste de structures"

    def __init__(self, *args, **kwargs):
        self.bot_user = User.objects.get_dora_bot()
        self.source = StructureSource.objects.get(value="invitations-masse")
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("filename")

        parser.add_argument(
            "-n",
            "--wet-run",
            action="store_true",
            help="Effectue l'opération de fichier et l'envoi de mail (mode 'dry-run' par défaut)",
        )

    def handle(self, *args, **options):
        filename = options["filename"]
        wet_run = options["wet_run"]

        if wet_run:
            self.stdout.write(self.style.WARNING("PRODUCTION RUN"))
        else:
            self.stdout.write(self.style.NOTICE("DRY RUN"))

        with open(filename) as structures_file:
            reader = csv.DictReader(structures_file, delimiter=",")
            # index à 1 et entête CSV
            for i, row in enumerate(reader, 2):
                serializer = ImportSerializer(
                    data={
                        "name": row["nom"],
                        "siret": row["siret"],
                        "parent_siret": row["siret_parent"],
                        "admins": to_string_array(row["courriels_administrateurs"]),
                        "labels": to_string_array(row["labels"]),
                        "models": to_string_array(row["modeles"]),
                        # champs optionnels correspondant directement
                        # à un champ du modèle structure
                        "phone": row.get("telephone", ""),
                        "email": row.get("courriel_structure", ""),
                    }
                )

                if serializer.is_valid():
                    data = serializer.validated_data
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{i}. Import de la structure {serializer.data['name']} (SIRET:{serializer.data['siret']})"
                        )
                    )
                    if wet_run:
                        structure = self.get_or_create_structure(
                            data["name"],
                            data["siret"],
                            data["parent_siret"],
                            phone=data.get("phone"),
                            email=data.get("email"),
                        )
                        self.stdout.write(f"{structure.get_frontend_url()}")
                        self.invite_users(structure, data["admins"])
                        self.add_labels(structure, data["labels"])
                        self.create_services(structure, data["models"])
                else:
                    self.stderr.write(
                        self.style.ERROR(pformat(dict(serializer.errors.items())))
                    )

    def get_or_create_structure(
        self,
        name,
        siret,
        parent_siret,
        **kwargs,
    ):
        if parent_siret:
            parent_structure = self._get_or_create_structure_from_siret(
                parent_siret, is_parent=True, **kwargs
            )
            structure = self._get_or_create_branch(
                name, siret, parent_structure, **kwargs
            )
        else:
            structure = self._get_or_create_structure_from_siret(siret, **kwargs)

        return structure

    def invite_users(self, structure, emails):
        for email in emails:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email,
                )
            try:
                member = StructurePutativeMember.objects.get(
                    user=user, structure=structure
                )
                self.stdout.write(f"{email} a déjà été invité·e")
                if not member.is_admin:
                    member.is_admin = True
                    member.save()
            except StructurePutativeMember.DoesNotExist:
                try:
                    member = StructureMember.objects.get(user=user, structure=structure)
                    self.stdout.write(f"{email} est déjà membre de la structure")
                    if not member.is_admin:
                        member.is_admin = True
                        member.save()
                except StructureMember.DoesNotExist:
                    member = StructurePutativeMember.objects.create(
                        user=user,
                        structure=structure,
                        invited_by_admin=True,
                        is_admin=True,
                    )

                    self.stdout.write(f"{email} invité·e comme administrateur·rice")
                    send_invitation_email(
                        member,
                        "L’équipe DORA",
                    )

    def add_labels(self, structure, labels):
        for label in labels:
            if label not in structure.national_labels.all():
                self.stdout.write(f"Ajout du label {label.value}")
                structure.national_labels.add(label)

    def create_services(self, structure, models):
        for model in models:
            if not structure.services.filter(model=model).exists():
                service = instantiate_model(model, structure, self.bot_user)
                self.stdout.write(
                    f"Ajout du service {service.name} ({service.get_frontend_url()})"
                )

    def _get_or_create_branch(self, name, siret, parent_structure, **kwargs):
        try:
            if siret:
                branch = Structure.objects.get(siret=siret)
            else:
                branch = Structure.objects.get(parent=parent_structure, name=name)

            self.stdout.write(
                f"La branche {branch.name} ({branch.get_frontend_url()}) existe déjà"
            )
        except Structure.DoesNotExist:
            if siret:
                establishment = Establishment.objects.get(siret=siret)
                branch = Structure.objects.create_from_establishment(
                    establishment, name, parent_structure, **kwargs
                )
            else:
                branch = Structure.objects.create(
                    name=name,
                    parent=parent_structure,
                    **kwargs,
                )
            parent_structure.post_create_branch(branch, self.bot_user, self.source)

            self.stdout.write(
                f"Création de la branche {branch.name} ({branch.get_frontend_url()})"
            )
            send_moderation_notification(
                branch,
                self.bot_user,
                "Structure créée à partir d'un import en masse",
                ModerationStatus.VALIDATED,
            )
        return branch

    def _get_or_create_structure_from_siret(self, siret, is_parent=False, **kwargs):
        try:
            structure = Structure.objects.get(siret=siret)
            self.stdout.write(
                f"La structure {'parente' if is_parent else ''} {structure.name} ({structure.get_frontend_url()}) existe déjà"
            )
            # certains champs comme le téléphone ou le courriel de structure
            # peuvent néanmoins être mis à jour lors d'un import,
            # même si la structure exite déjà
            self._update_optional_fields(structure, **kwargs)
        except Structure.DoesNotExist:
            establishment = Establishment.objects.get(siret=siret)
            structure = Structure.objects.create_from_establishment(
                establishment, **kwargs
            )
            structure.creator = self.bot_user
            structure.last_editor = self.bot_user
            structure.source = self.source
            structure.save()

            self.stdout.write(
                f"Création de la structure  {'parente' if is_parent else ''} {structure.name} ({structure.get_frontend_url()})"
            )
            send_moderation_notification(
                structure,
                self.bot_user,
                "Structure créée à partir d'un import en masse",
                ModerationStatus.VALIDATED,
            )

        return structure

    def _update_optional_fields(self, structure, **kwargs):
        # Même si la structure existe déjà,
        # les champs optionnels peuvent être mis à jour si ils contiennent une valeur
        to_update = dict({(k, v) for k, v in kwargs.items() if v})
        self.stdout.write(f" > mise à jour des champs : {to_update}")
        Structure.objects.filter(pk=structure.pk).update(**to_update)
