import csv
from pprint import pformat
from typing import Dict, List, Union

from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers

from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.utils import skip_csv_lines
from dora.core.validators import validate_phone_number, validate_siret
from dora.services.models import ServiceModel
from dora.services.utils import instantiate_service_from_model
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


class ImportStructuresHelper:
    def __init__(self, *args, **kwargs) -> None:
        self.source = None
        self.importing_user = None
        self._initialize_trackers()

    def _initialize_trackers(self) -> None:
        self.map_line_to_errors = {}
        self.created_structures_count = 0
        self.created_services_count = 0
        self.edited_structures_count = 0
        self.invited_users = {}

    def import_structures(
        self,
        reader: csv.reader,
        importing_user: User,
        source_info: Dict[str, str],
        wet_run: bool = False,
        should_remove_first_two_lines: bool = False,
        progress_callback=None,
    ) -> Dict[str, Union[Dict[int, List[str]], int]]:
        if wet_run:
            print("⚠️ PRODUCTION RUN ⚠️")
        else:
            print("🧘 DRY RUN 🧘")

        self._initialize_trackers()
        self.importing_user = importing_user

        csv_reader = (
            skip_csv_lines(reader, 2) if should_remove_first_two_lines else reader
        )

        [headers, *lines] = csv_reader

        missing_headers = set(self.CSV_HEADERS) - set(headers)

        if missing_headers:
            headers_list = "<br/>".join(f"• {header}" for header in missing_headers)
            error_message = f"Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/> {
                headers_list
            }"

            print(error_message)
            return {"errors_map": {1: [error_message]}}

        lines = [dict(zip(headers, line)) for line in lines]
        for idx, line in enumerate(lines, 2):
            serializer = ImportSerializer(
                data={
                    "name": line["nom"],
                    "siret": line["siret"],
                    "parent_siret": line["siret_parent"],
                    "admins": self._to_string_array(line["courriels_administrateurs"]),
                    "labels": self._to_string_array(line["labels"]),
                    "models": self._to_string_array(line["modeles"]),
                    # champs optionnels correspondant directement
                    # à un champ du modèle structure
                    "phone": line.get("telephone", ""),
                    "email": line.get("courriel_structure", ""),
                }
            )

            if serializer.is_valid():
                data = serializer.validated_data
                msg = f"{idx}. Import de la structure {serializer.data['name']} (SIRET:{serializer.data['siret']})"
                print(msg)
                if progress_callback:
                    progress_callback(msg)
                if wet_run:
                    try:
                        self._get_structure_source(source_info)
                    except IntegrityError:
                        error_message = f'Le fichier nommé "{source_info["value"]}" a déjà un nom de source stocké dans le base de données. Veuillez refaire l\'import avec un nouveau nom de source.'
                        print(error_message)
                        return {"errors_map": {1: [error_message]}}

                    structure = self.get_or_create_structure(
                        data["name"],
                        data["siret"],
                        data["parent_siret"],
                        importing_user,
                        phone=data.get("phone"),
                        email=data.get("email"),
                    )
                    print(f"{structure.get_frontend_url()}")
                    self.invite_users(structure, data["admins"])
                    self.add_labels(structure, data["labels"])
                    self.create_services(structure, data["models"], importing_user)
            else:
                self.map_line_to_errors[idx] = [
                    str(error[0]) for error in serializer.errors.values()
                ]
                print(pformat(dict(serializer.errors.items())))
        return {
            "errors_map": self.map_line_to_errors,
            "created_structures_count": self.created_structures_count,
            "created_services_count": self.created_services_count,
            "edited_structures_count": self.edited_structures_count,
        }

    def get_or_create_structure(
        self,
        name: str,
        siret: str,
        parent_siret: str,
        importing_user: User,
        **kwargs,
    ) -> Structure:
        if parent_siret:
            parent_structure = self._get_or_create_structure_from_siret(
                parent_siret, importing_user, is_parent=True, **kwargs
            )
            structure = self._get_or_create_branch(
                name, siret, parent_structure, **kwargs
            )
        else:
            structure = self._get_or_create_structure_from_siret(
                siret, importing_user, **kwargs
            )

        return structure

    def invite_users(self, structure: Structure, emails: List[str]) -> None:
        for email in emails:
            try:
                user = User.objects.get_by_email(email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email,
                )
            try:
                member = StructurePutativeMember.objects.get(
                    user=user, structure=structure
                )
                print(f"{email} a déjà été invité·e")
                if not member.is_admin:
                    member.is_admin = True
                    member.save()
            except StructurePutativeMember.DoesNotExist:
                try:
                    member = StructureMember.objects.get(user=user, structure=structure)
                    print(f"{email} est déjà membre de la structure")
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

                    print(f"{email} invité·e comme administrateur·rice")
                    send_invitation_email(
                        member,
                        "L’équipe DORA",
                    )

    def add_labels(
        self, structure: Structure, labels: List[StructureNationalLabel]
    ) -> None:
        for label in labels:
            if label not in structure.national_labels.all():
                print(f"Ajout du label {label.value}")
                structure.national_labels.add(label)

    def create_services(
        self, structure: Structure, models: List[ServiceModel], importing_user: User
    ) -> None:
        for model in models:
            if not structure.services.filter(model=model).exists():
                service = instantiate_service_from_model(
                    model, structure, importing_user
                )
                print(f"Ajout du service {service.name} ({service.get_frontend_url()})")
                self.created_services_count += 1

    def _get_or_create_branch(
        self, name: str, siret: str, parent_structure: Structure, **kwargs
    ) -> Structure:
        try:
            if siret:
                branch = Structure.objects.get(siret=siret)
            else:
                branch = Structure.objects.get(parent=parent_structure, name=name)

            print(f"L'antenne {branch.name} ({branch.get_frontend_url()}) existe déjà")
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
            parent_structure.post_create_branch(
                branch, self.importing_user, self.source
            )
            self.created_structures_count += 1

            print(f"Création de l'antenne {branch.name} ({branch.get_frontend_url()})")
            send_moderation_notification(
                branch,
                self.importing_user,
                "Structure créée à partir d'un import en masse",
                ModerationStatus.VALIDATED,
            )
        return branch

    def _get_or_create_structure_from_siret(
        self, siret: str, importing_user: User, is_parent: bool = False, **kwargs
    ) -> Structure:
        try:
            structure = Structure.objects.get(siret=siret)
            print(
                f"La structure {'parente' if is_parent else ''} {structure.name} ({structure.get_frontend_url()}) existe déjà"
            )
            if not is_parent and any(value for value in kwargs.values()):
                self._update_optional_fields(structure, **kwargs)
        except Structure.DoesNotExist:
            establishment = Establishment.objects.get(siret=siret)
            structure = Structure.objects.create_from_establishment(
                establishment, **kwargs
            )
            structure.creator = importing_user
            structure.last_editor = importing_user
            structure.source = self.source
            structure.save()

            print(
                f"Création de la structure  {'parente' if is_parent else ''} {structure.name} ({structure.get_frontend_url()})"
            )
            self.created_structures_count += 1
            send_moderation_notification(
                structure,
                importing_user,
                "Structure créée à partir d'un import en masse",
                ModerationStatus.VALIDATED,
            )

        return structure

    def _update_optional_fields(self, structure: Structure, **kwargs) -> None:
        # Même si la structure existe déjà,
        # les champs optionnels (comme le téléphone et l'adresse mail) peuvent être mis à jour s'ils contiennent une valeur
        to_update = dict({(k, v) for k, v in kwargs.items() if v})
        print(f" > mise à jour des champs : {to_update}")
        Structure.objects.filter(pk=structure.pk).update(
            **to_update,
            modification_date=timezone.now(),
            last_editor=self.importing_user,
        )
        self.edited_structures_count += 1

    def _to_string_array(self, strings_list: str) -> List[str]:
        clean_str = strings_list.strip()
        if clean_str:
            return [value.strip() for value in clean_str.split(",")]
        return []

    CSV_HEADERS = [
        "nom",
        "siret",
        "siret_parent",
        "courriels_administrateurs",
        "labels",
        "modeles",
        "telephone",
        "courriel_structure",
    ]

    def _get_structure_source(self, source_info: Dict[str, str]) -> None:
        source, _ = StructureSource.objects.get_or_create(
            value=source_info["value"],
            label=source_info["label"],
        )
        self.source = source


class ImportSerializer(serializers.Serializer):
    name = serializers.CharField(
        error_messages={
            "blank": 'La colonne "nom" est obligatoire',
            "required": 'La colonne "nom" est obligatoire',
        }
    )
    siret = serializers.CharField(allow_blank=True, validators=[validate_siret])
    parent_siret = serializers.CharField(allow_blank=True, validators=[validate_siret])
    admins = serializers.ListField(child=serializers.EmailField(), allow_empty=True)
    labels = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    models = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    phone = serializers.CharField(allow_blank=True, validators=[validate_phone_number])
    email = serializers.EmailField(allow_blank=True)

    def _clean_siret_or_phone(self, siret_or_phone: str) -> str:
        if not siret_or_phone:
            return ""
        return "".join([c for c in siret_or_phone if c.isdigit()])

    def to_internal_value(self, data: Dict) -> Dict:
        # nettoyage pré-validation
        data |= {
            "siret": self._clean_siret_or_phone(data["siret"]),
            "phone": self._clean_siret_or_phone(data["phone"]),
            "parent_siret": self._clean_siret_or_phone(data["parent_siret"]),
        }

        return super().to_internal_value(data)

    def validate_siret(self, siret: str) -> str:
        if (
            siret
            and not Structure.objects.filter(siret=siret).exists()
            and not Establishment.objects.filter(siret=siret).exists()
        ):
            raise serializers.ValidationError(
                f"Siret inconnu: https://annuaire-entreprises.data.gouv.fr/etablissement/{siret}"
            )
        return siret

    def validate_parent_siret(self, parent_siret: str) -> str:
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

    def validate(self, data: Dict) -> Dict:
        siret = data.get("siret")
        parent_siret = data.get("parent_siret")

        if not siret and not parent_siret:
            raise serializers.ValidationError("`siret` ou `parent_siret` sont requis")

        return super().validate(data)

    def validate_labels(self, label_slugs: List[str]) -> List[StructureNationalLabel]:
        labels = []
        for label in label_slugs:
            try:
                label_obj = StructureNationalLabel.objects.get(value=label)
                labels.append(label_obj)
            except StructureNationalLabel.DoesNotExist:
                raise serializers.ValidationError(f"Label inconnu {label}")
        return labels

    def validate_models(self, model_slugs: List[str]) -> List[ServiceModel]:
        models = []
        for slug in model_slugs:
            try:
                model = ServiceModel.objects.get(slug=slug)
                models.append(model)
            except ServiceModel.DoesNotExist:
                raise serializers.ValidationError(f"Modèle inconnu {slug}")
        return models
