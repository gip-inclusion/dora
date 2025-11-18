import json
from io import StringIO

import requests
from data_inclusion.schema.v0 import TypologieStructure
from django.conf import settings
from django.utils import timezone
from yachalk import chalk

from dora.admin_express.utils import get_clean_city_name
from dora.core.commands import BaseCommand
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.utils import normalize_phone_number
from dora.structures.models import Structure, StructureNationalLabel, StructureSource
from dora.users.models import User


def get_ft_credentials():
    # https://francetravail.io/data/documentation/utilisation-api-pole-emploi/generer-access-token
    try:
        response = requests.post(
            url="https://entreprise.francetravail.fr/connexion/oauth2/access_token",
            params={
                "realm": "/partenaire",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": settings.FT_CLIENT_ID,
                "client_secret": settings.FT_CLIENT_SECRET,
                "scope": f"application_{settings.FT_CLIENT_ID} api_referentielagencesv1 organisationpe",
            },
        )
        return json.loads(response.content)
    except requests.exceptions.RequestException:
        print("HTTP Request failed")


def get_ft_agencies(token):
    # https://francetravail.io/data/api/referentiel-agences
    try:
        response = requests.get(
            url="https://api.francetravail.io/partenaire/referentielagences/v1/agences",
            params={},
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        return json.loads(response.content)
    except requests.exceptions.RequestException:
        print("HTTP Request failed")


def get_structure_info(structure, prefix):
    return (
        f"{prefix} {structure.name}\n"
        f"{' ' * len(prefix)} siret : {structure.siret}, safir : {structure.code_safir_ft}\n"
        f"{' ' * len(prefix)} {structure.get_admin_url()}\n"
        f"{' ' * len(prefix)} https://annuaire-entreprises.data.gouv.fr/etablissement/{structure.siret}\n"
    )


class Command(BaseCommand):
    help = "Importe les agences Pôle emploi dans la table des Structures, en utilisant l’API “Référentiel des agences”"

    def __init__(self, *args, **kwargs):
        self.tmpout = None
        super().__init__(args, kwargs)

    def handle(self, *args, **options):
        self.stdout.write("Authentification à l’API Pôle emploi…")
        ft_access_token = get_ft_credentials()["access_token"]
        self.stdout.write("Récupération de la liste des agences Pôle emploi…")
        agencies = get_ft_agencies(ft_access_token)

        bot_user = User.objects.get_dora_bot()
        label = StructureNationalLabel.objects.get(value="france-travail")
        source = StructureSource.objects.get(
            value="api-referentiel-agences-france-travail"
        )

        created_count = 0
        modified_count = 0
        untouched_count = 0

        for agency in agencies:
            self.tmpout = StringIO()
            try:
                if not agency.get("siret"):
                    # self.tmpout.write(chalk.red("Siret manquant dans l’API\n"))
                    continue
                if not agency.get("codeSafir"):
                    # self.tmpout.write(chalk.red("Code Safir manquant dans l’API\n"))
                    continue

                try:
                    siret = agency.get("siret")
                    safir = agency.get("codeSafir")

                    s_from_siret = Structure.objects.filter(siret=siret).first()
                    s_from_safir = Structure.objects.filter(code_safir_ft=safir).first()
                    if s_from_safir and s_from_siret and s_from_safir != s_from_siret:
                        self.log_agency_error(
                            "Il existe déjà une structure ayant ce siret mais un code safir différent, "
                            "et une structure ayant ce code safir mais un siret different",
                            s_from_siret,
                            s_from_safir,
                        )
                        continue
                    elif s_from_safir and not s_from_siret:
                        self.log_agency_error(
                            "Il existe déjà une structure ayant ce code safir, mais un siret different",
                            s_from_safir,
                        )
                        continue
                    elif (
                        s_from_siret
                        and s_from_siret.code_safir_ft
                        and s_from_siret.code_safir_ft != safir
                    ):
                        self.log_agency_error(
                            "Il existe déjà une structure ayant ce siret mais un code safir différent",
                            s_from_siret,
                        )
                        continue

                    structure = (
                        s_from_siret
                        if s_from_siret
                        else Structure.objects.create(
                            siret=agency.get("siret"),
                            name=agency.get("libelleEtendu"),
                            code_safir_ft=agency.get("codeSafir"),
                        )
                    )

                    existing = bool(s_from_siret)

                    if not existing:
                        # Il s’agit d’une nouvelle structure
                        structure.source = source
                        structure.creator = bot_user
                        send_moderation_notification(
                            structure,
                            bot_user,
                            "Structure créée à partir de l’API France Travail",
                            ModerationStatus.VALIDATED,
                        )

                    mod = self.maybe_update(
                        structure,
                        "code_safir_ft",
                        agency.get("codeSafir"),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "typology",
                        TypologieStructure.FT.value,
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure, "name", agency.get("libelleEtendu", ""), existing
                    )
                    mod |= self.maybe_update(
                        structure,
                        "phone",
                        normalize_phone_number(
                            agency["contact"].get("telephonePublic", "")
                        ),
                        existing,
                    )
                    # Attention: on ne veut à priori pas exposer l'email des agences
                    # mod |= self.maybe_update(
                    #     structure,
                    #     "email",
                    #     agency["contact"].get("email", ""),
                    #     existing,
                    # )
                    address = agency.get("adressePrincipale")
                    mod |= self.maybe_update(
                        structure,
                        "postal_code",
                        address.get("bureauDistributeur", ""),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "city_code",
                        address.get("communeImplantation", ""),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "city",
                        get_clean_city_name(address.get("communeImplantation", "")),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "address1",
                        address.get("ligne4", ""),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "address2",
                        address.get("ligne5", ""),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "longitude",
                        address.get("gpsLon"),
                        existing,
                    )
                    mod |= self.maybe_update(
                        structure,
                        "latitude",
                        address.get("gpsLat"),
                        existing,
                    )

                    if label not in structure.national_labels.all():
                        structure.national_labels.add(label)
                        mod = True

                    if mod:
                        structure.last_editor = bot_user
                        structure.modification_date = timezone.now()
                        structure.save()

                    if not existing:
                        created_count += 1
                    elif mod:
                        modified_count += 1
                    else:
                        untouched_count += 1

                except KeyError as err:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Missing field {err} for {agency.get('code')} - {agency.get('libelleEtendu')}"
                        )
                    )
                    print(agency)
                    continue
                except Exception as err:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Exception for {agency.get('code')} - {agency.get('libelleEtendu')}"
                        )
                    )
                    print(err)
                    print(agency)
                    raise err
            finally:
                output = self.tmpout.getvalue()
                if len(output):
                    self.stdout.write(
                        f"{chalk.bold(agency.get('libelleEtendu'))} (siret : {agency.get('siret')}, "
                        f"safir : {agency.get('codeSafir')})"
                    )
                    self.stdout.write(output)

        self.stdout.write(f"Structures créées : {created_count}")
        self.stdout.write(f"Structures modifiées : {modified_count}")
        self.stdout.write(f"Structures ignorées : {untouched_count}")

    def maybe_update(self, structure, target_field, new_value, show_diff):
        previous_value = getattr(structure, target_field)
        if previous_value != new_value:
            if show_diff:
                self.tmpout.write(
                    f"Champ {target_field} modifié : {previous_value} => {new_value}\n"
                )
            setattr(structure, target_field, new_value)
            return True
        return False

    def log_agency_error(self, message, structure, other_structure=None):
        self.tmpout.write(chalk.red(message) + "\n")
        if structure:
            self.tmpout.write(get_structure_info(structure, "Structure 1 : "))
        if other_structure:
            self.tmpout.write(get_structure_info(other_structure, "Structure 2 : "))
