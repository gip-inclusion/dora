import pytest
from data_inclusion.schema.v0 import TypologieStructure
from data_inclusion.schema.v1.publics import Public as DiPublic
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.utils.timezone import timedelta
from model_bakery import baker

from dora.admin_express.models import City, Department
from dora.core.constants import WGS84
from dora.core.test_utils import make_service, make_structure, make_user
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    Credential,
    LocationKind,
    Public,
    Requirement,
    ServiceFee,
    ServiceKind,
    ServiceStatus,
    ServiceSubCategory,
)
from dora.structures.models import StructureNationalLabel, StructureSource


@pytest.fixture
def authenticated_user(api_client, settings):
    user = baker.make("users.User", is_valid=True, email=settings.DATA_INCLUSION_EMAIL)
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def setup_structure_data():
    baker.make("structures.StructureSource", value="solidagregateur")
    baker.make("structures.StructureNationalLabel", value="MOBIN")
    baker.make("structures.StructureNationalLabel", value="AFPA")
    baker.make("City", name="Robinboeuf CEDEX", code="09890")


# API publique : structures


def test_structures_api_response_need_di_user(api_client):
    response = api_client.get("/api/v2/structures/")

    assert 401 == response.status_code


def test_structures_api_response(authenticated_user, api_client):
    response = api_client.get("/api/v2/structures/")

    assert 200, response.status_code
    assert [] == response.data


# TODO: plus tard ...
# @pytest.mark.loaddata("structure_typology", "service_subcategory")
def test_structures_serialization_exemple(
    setup_structure_data, authenticated_user, api_client, settings
):
    # Example adapté de la doc data·inclusion :
    # https://www.data.inclusion.beta.gouv.fr/schemas-de-donnees-de-loffre/schema-des-structures-et-services-dinsertion
    typology = TypologieStructure.ASSO
    source = StructureSource.objects.get(value="solidagregateur")
    parent = make_structure()

    struct = make_structure(
        siret="60487647500499",
        # rna="W123456789",
        name="MOBILETTE",
        # city="Robinboeuf CEDEX",
        postal_code="09891",
        city_code="09890",
        address1="RUE DE LECLERCQ",
        address2="HOTEL DE VILLE",
        longitude=7.848133,
        latitude=48.7703,
        typology=typology.value,
        phone="0102030405",
        email="julie@example.net",
        url="https://www.asso-gonzalez.net/",
        short_desc="L’association Mobilette propose des solutions de déplacement aux personnes pour qui la non mobilité est un frein à l’insertion professionnelle : - connaissance de l'offre de transport du territoire - accès à un véhicule 2 ou 4 roues - transport solidaire - accès au permis",
        full_desc="",
        source=source,
        parent=parent,
        opening_hours='Mo-Fr 10:00-20:00 "sur rendez-vous"; PH off',
        accesslibre_url="https://acceslibre.beta.gouv.fr/app/29-lampaul-plouarzel/a/bibliotheque-mediatheque/erp/mediatheque-13/",
        other_labels=[
            "Nièvre médiation numérique",
        ],
    )
    struct.modification_date = "2022-04-28T16:53:11Z"
    struct.national_labels.add(
        StructureNationalLabel.objects.get(value="MOBIN"),
        StructureNationalLabel.objects.get(value="AFPA"),
    )
    s1 = make_service(structure=struct, status=ServiceStatus.PUBLISHED)
    s1.subcategories.add(
        ServiceSubCategory.objects.get(
            value="choisir-un-metier--confirmer-son-choix-de-metier"
        )
    )
    s2 = make_service(structure=struct, status=ServiceStatus.PUBLISHED)
    s2.subcategories.add(
        ServiceSubCategory.objects.get(
            value="mobilite--entretenir-reparer-son-vehicule"
        )
    )
    struct.save()
    response = api_client.get(f"/api/v2/structures/{struct.id}/")

    assert 200 == response.status_code
    assert response.json() == {
        "accessibilite": "https://acceslibre.beta.gouv.fr/app/29-lampaul-plouarzel/a/bibliotheque-mediatheque/erp/mediatheque-13/",
        "adresse": "RUE DE LECLERCQ",
        "antenne": True,
        "code_insee": "09890",
        "code_postal": "09891",
        "commune": "Robinboeuf CEDEX",
        "complement_adresse": "HOTEL DE VILLE",
        "courriel": "julie@example.net",
        "date_maj": "2022-04-28T16:53:11Z",
        "horaires_ouverture": 'Mo-Fr 10:00-20:00 "sur rendez-vous"; PH off',
        "id": str(struct.id),
        "labels_autres": ["Nièvre médiation numérique"],
        "labels_nationaux": ["MOBIN", "AFPA"],
        "latitude": 48.7703,
        "lien_source": f"{settings.FRONTEND_URL}/structures/{struct.slug}",
        "longitude": 7.848133,
        "nom": "MOBILETTE",
        "presentation_detail": None,
        "presentation_resume": "L’association Mobilette propose des solutions de déplacement aux personnes pour qui la non mobilité est un frein à l’insertion professionnelle : - connaissance de l'offre de transport du territoire - accès à un véhicule 2 ou 4 roues - transport solidaire - accès au permis",
        "rna": None,
        "siret": "60487647500499",
        "parent_siret": parent.siret,
        "site_web": "https://www.asso-gonzalez.net/",
        "source": "solidagregateur",
        "telephone": "0102030405",
        "thematiques": None,
        "typologie": "ASSO",
    }


# API publique : services


def test_services_api_response(authenticated_user, api_client):
    response = api_client.get("/api/v2/services/")

    assert 200 == response.status_code
    assert [] == response.data


def test_services_api_response_need_di_user(api_client):
    response = api_client.get("/api/v2/services/")

    assert 401 == response.status_code


def test_unpublished_service_is_not_serialized(authenticated_user, api_client):
    service = make_service(status=ServiceStatus.DRAFT)
    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 404 == response.status_code


# TODO: plus tard ...
# @pytest.mark.loaddata(
#     "service_fee",
#     "service_subcategory",
#     "service_kind",
#     "service_location_kind",
#     "service_coach_orientation_mode",
#     "service_beneficiary_access_mode",
# )
def test_service_serialization_exemple(authenticated_user, api_client, settings):
    # Example adapté de la doc data·inclusion :
    # https://www.data.inclusion.beta.gouv.fr/schemas-de-donnees-de-loffre/schema-des-structures-et-services-dinsertion
    baker.make(Department, code="29", name="Finistère")
    baker.make(City, code="29188", name="Plougasnou")

    user = make_user()
    structure = make_structure(user=user)
    service = make_service(
        structure=structure,
        status=ServiceStatus.PUBLISHED,
        name="TISF",
        short_desc="Accompagnement des familles à domicile",
        full_desc="Service de proximité visant à soutenir les familles ayant la responsabilité de jeunes enfants, en particulier les familles monoparentales.",
        fee_condition=ServiceFee.objects.get(value="payant"),
        fee_details="10 €",
        diffusion_zone_type="department",
        diffusion_zone_details="29",
        address1="25 route de Morlaix",
        city_code="29188",
        postal_code="29630",
        contact_name="Prénom Nom",
        contact_email="contact@alys.fr",
        contact_phone="0278911262",
        is_contact_info_public=True,
        publication_date="2023-02-04T12:34:44Z",
        modification_date="2023-03-11T16:54:10Z",
        geom=Point(3.76855, 23.88654, srid=WGS84),
        recurrence="Tu 09:00-12:00;We 14:00-17:00",
        coach_orientation_modes_other="Mêmes modalités que pour les bénéficiaires",
        beneficiaries_access_modes_other="Contacter conseiller(e) Pôle Emploi",
        appointment_link="https://example.com",
    )

    service.subcategories.add(
        ServiceSubCategory.objects.get(
            value="choisir-un-metier--confirmer-son-choix-de-metier"
        )
    )
    service.kinds.add(
        ServiceKind.objects.get(value="formation"),
        ServiceKind.objects.get(value="information"),
    )
    service.publics.add(
        baker.make(
            Public, name="familles", corresponding_di_publics=[DiPublic.FAMILLES]
        ),
        baker.make(
            Public, name="etudiants", corresponding_di_publics=[DiPublic.ETUDIANTS]
        ),
        baker.make(Public, name="femmes", corresponding_di_publics=[DiPublic.FEMMES]),
    )
    service.location_kinds.add(LocationKind.objects.get(value="en-presentiel"))
    service.location_kinds.add(LocationKind.objects.get(value="a-distance"))
    service.requirements.add(
        baker.make(Requirement, name="Bonne connaissance du français oral et écrit"),
    )
    service.credentials.add(
        baker.make(Credential, name="Carte d'identité, passeport ou permis de séjour"),
    )
    service.coach_orientation_modes.add(
        CoachOrientationMode.objects.get(value="envoyer-un-mail"),
        CoachOrientationMode.objects.get(value="formulaire-dora"),
        CoachOrientationMode.objects.get(
            value="envoyer-un-mail-avec-une-fiche-de-prescription"
        ),
    )
    service.beneficiaries_access_modes.add(
        BeneficiaryAccessMode.objects.get(value="envoyer-un-mail")
    )

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 200 == response.status_code
    assert response.json() == {
        "adresse": "25 route de Morlaix",
        "code_insee": "29188",
        "code_postal": "29630",
        "commune": "Plougasnou",
        "complement_adresse": None,
        "contact_nom_prenom": "Prénom Nom",
        "contact_public": True,
        "courriel": "contact@alys.fr",
        "cumulable": True,
        "date_creation": "2023-02-04T12:34:44Z",
        "date_maj": "2023-03-11T16:54:10Z",
        "date_suspension": None,
        "temps_passe_duree_hebdomadaire": None,
        "temps_passe_semaines": None,
        "formulaire_en_ligne": service.get_dora_form_url(),
        "frais_autres": "10 €",
        "frais": "payant",
        "id": str(service.id),
        "justificatifs": ["Carte d'identité, passeport ou permis de séjour"],
        "latitude": 23.88654,
        "lien_source": f"{settings.FRONTEND_URL}/services/{service.slug}",
        "longitude": 3.76855,
        "modes_accueil": ["a-distance", "en-presentiel"],
        "nom": "TISF",
        "pre_requis": ["Bonne connaissance du français oral et écrit"],
        "presentation_detail": "Service de proximité visant à soutenir les familles ayant la responsabilité de jeunes enfants, en particulier les familles monoparentales.",
        "presentation_resume": "Accompagnement des familles à domicile",
        "prise_rdv": "https://example.com",
        "profils": ["familles", "etudiants", "femmes"],
        "publics": ["familles", "etudiants", "femmes"],
        "publics_precisions": "familles, etudiants, femmes",
        "recurrence": "Tu 09:00-12:00;We 14:00-17:00",
        "source": None,
        "structure_id": str(structure.id),
        "telephone": "0278911262",
        "thematiques": ["choisir-un-metier--confirmer-son-choix-de-metier"],
        "types": [
            "formation",
            "information",
        ],
        "zone_diffusion_code": "29",
        "zone_diffusion_nom": "Finistère",
        "zone_diffusion_type": "departement",
        "modes_orientation_accompagnateur": [
            "completer-le-formulaire-dadhesion",
            "envoyer-un-mail",
            "envoyer-un-mail-avec-une-fiche-de-prescription",
        ],
        "modes_orientation_accompagnateur_autres": "Mêmes modalités que pour les bénéficiaires",
        "modes_orientation_beneficiaire": ["envoyer-un-mail"],
        "modes_orientation_beneficiaire_autres": "Contacter conseiller(e) Pôle Emploi",
    }


def test_service_serialization_formulaire_en_ligne(
    authenticated_user, api_client, settings
):
    # Initialisation du service
    service = make_service(status=ServiceStatus.PUBLISHED)
    service.coach_orientation_modes.clear()
    service.coach_orientation_modes_external_form_link = "http://example.com/coach-form"
    service.coach_orientation_modes.add(
        CoachOrientationMode.objects.get(value="formulaire-dora"),
        CoachOrientationMode.objects.get(value="completer-le-formulaire-dadhesion"),
    )
    service.beneficiaries_access_modes.clear()
    service.beneficiaries_access_modes.add(
        BeneficiaryAccessMode.objects.get(value="completer-le-formulaire-dadhesion")
    )
    service.beneficiaries_access_modes_external_form_link = (
        "http://example.com/beneficiary-form"
    )
    service.online_form = "http://example.com/online-form"
    service.save()

    # Formulaire en ligne = formulaire accompagnateur
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] == "http://example.com/coach-form"

    # Formulaire en ligne = formulaire bénéficiaire
    service.coach_orientation_modes.remove(
        CoachOrientationMode.objects.get(value="completer-le-formulaire-dadhesion")
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] == "http://example.com/beneficiary-form"

    # Formulaire en ligne = formulaire DORA
    service.beneficiaries_access_modes.remove(
        BeneficiaryAccessMode.objects.get(value="completer-le-formulaire-dadhesion")
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] == service.get_dora_form_url()

    # Formulaire en ligne = lien documents
    service.coach_orientation_modes.remove(
        CoachOrientationMode.objects.get(value="formulaire-dora")
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] == "http://example.com/online-form"

    # Formulaire en ligne = aucun
    service.online_form = ""
    service.save()
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] is None


def test_service_serialization_exemple_need_di_user(api_client):
    baker.make(Department, code="29", name="Finistère")
    baker.make(City, code="29188", name="Plougasnou")

    structure = make_structure()
    service = make_service(
        structure=structure,
        status=ServiceStatus.PUBLISHED,
        name="TISF",
        short_desc="Accompagnement des familles à domicile",
        full_desc="Service de proximité visant à soutenir les familles ayant la responsabilité de jeunes enfants, en particulier les familles monoparentales.",
        fee_condition=ServiceFee.objects.get(value="payant"),
        fee_details="10 €",
        diffusion_zone_type="department",
        diffusion_zone_details="29",
        address1="25 route de Morlaix",
        city_code="29188",
        postal_code="29630",
        contact_name="Prénom Nom",
        contact_email="contact@alys.fr",
        contact_phone="0278911262",
        is_contact_info_public=True,
        publication_date="2023-02-04T12:34:44Z",
        modification_date="2023-03-11T16:54:10Z",
        geom=Point(3.76855, 23.88654, srid=WGS84),
        recurrence="Tu 09:00-12:00;We 14:00-17:00",
    )

    service.subcategories.add(
        ServiceSubCategory.objects.get(
            value="choisir-un-metier--confirmer-son-choix-de-metier"
        )
    )
    service.kinds.add(
        ServiceKind.objects.get(value="formation"),
        ServiceKind.objects.get(value="information"),
    )
    service.publics.add(
        baker.make(
            Public, name="familles", corresponding_di_publics=[DiPublic.FAMILLES]
        ),
        baker.make(
            Public, name="etudiants", corresponding_di_publics=[DiPublic.ETUDIANTS]
        ),
        baker.make(Public, name="femmes", corresponding_di_publics=[DiPublic.FEMMES]),
    )
    service.location_kinds.add(LocationKind.objects.get(value="en-presentiel"))
    service.location_kinds.add(LocationKind.objects.get(value="a-distance"))
    service.requirements.add(
        baker.make(Requirement, name="Bonne connaissance du français oral et écrit"),
    )
    service.credentials.add(
        baker.make(Credential, name="Carte d'identité, passeport ou permis de séjour"),
    )

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 401 == response.status_code


def test_subcategories_other_excluded(authenticated_user, api_client):
    # Example adapté de la doc data·inclusion :
    # https://www.data.inclusion.beta.gouv.fr/schemas-de-donnees-de-loffre/schema-des-structures-et-services-dinsertion
    user = make_user()
    structure = make_structure(user=user)
    service = make_service(
        structure=structure,
        name="TISF",
        short_desc="Accompagnement des familles à domicile",
        fee_details="",
        status=ServiceStatus.PUBLISHED,
    )
    service.subcategories.add(
        ServiceSubCategory.objects.get(
            value="mobilite--entretenir-reparer-son-vehicule"
        )
    )
    ServiceSubCategory.objects.create(value="mobilite--autre", label="Autre")
    service.subcategories.add(ServiceSubCategory.objects.get(value="mobilite--autre"))

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 200 == response.status_code
    assert response.json().get("thematiques") == [
        "mobilite--entretenir-reparer-son-vehicule"
    ]


def test_service_from_obsolete_structure_is_excluded(authenticated_user, api_client):
    user = make_user()
    structure = make_structure(user=user)
    structure.is_obsolete = True
    structure.save()
    service = make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 404 == response.status_code


def test_service_from_orphan_structure_is_excluded(authenticated_user, api_client):
    structure = make_structure(user=None)
    structure.save()
    service = make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 404 == response.status_code


def test_service_with_suspension_date_in_the_past_is_excluded(
    authenticated_user, api_client
):
    service = make_service(
        status=ServiceStatus.PUBLISHED,
        suspension_date=timezone.now() - timedelta(days=1),
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert 404 == response.status_code


def test_service_with_suspension_date_in_the_future_is_included(
    authenticated_user, api_client
):
    service = make_service(
        status=ServiceStatus.PUBLISHED,
        suspension_date=timezone.now() + timedelta(days=1),
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert 200 == response.status_code


def test_service_without_suspension_date_is_included(authenticated_user, api_client):
    service = make_service(status=ServiceStatus.PUBLISHED, suspension_date=None)
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert 200 == response.status_code
