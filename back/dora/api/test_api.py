import pytest
from data_inclusion.schema.v1 import ModeAccueil
from data_inclusion.schema.v1.publics import Public as DiPublic
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.utils.timezone import timedelta
from model_bakery import baker

from dora.core.constants import WGS84
from dora.core.test_utils import make_service, make_structure, make_user
from dora.data_inclusion.enums import TypologieStructure
from dora.decoupage_administratif.models import City, Department
from dora.services.enums import ModeMobilisation, PersonneMobilisatrice
from dora.services.models import (
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
    baker.make("decoupage_administratif.City", name="Robinboeuf CEDEX", code="09890")


# API publique : structures


def test_structures_api_response_need_di_user(api_client):
    response = api_client.get("/api/v2/structures/")

    assert 401 == response.status_code


def test_structures_api_response(authenticated_user, api_client):
    response = api_client.get("/api/v2/structures/")

    assert 200, response.status_code
    assert [] == response.data


def test_structure_with_published_service_is_included(authenticated_user, api_client):
    """Structure avec au moins un service publié est incluse (même sans membre)"""
    structure = make_structure(user=None)
    make_service(structure=structure, status=ServiceStatus.PUBLISHED)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) in structure_ids


def test_structure_with_published_service_and_member_is_included(
    authenticated_user, api_client
):
    """Structure avec service publié ET membre réel est incluse"""
    user = make_user()
    structure = make_structure(user=user)
    make_service(structure=structure, status=ServiceStatus.PUBLISHED)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) in structure_ids


def test_structure_without_published_service_but_with_member_is_included(
    authenticated_user, api_client
):
    """Structure sans service publié mais avec au moins un membre réel est incluse"""
    user = make_user()
    structure = make_structure(user=user)
    # Pas de service publié, seulement un brouillon
    make_service(structure=structure, status=ServiceStatus.DRAFT)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) in structure_ids


def test_structure_without_published_service_and_without_member_is_excluded(
    authenticated_user, api_client
):
    """Structure sans service publié et sans membre réel est exclue"""
    structure = make_structure(user=None)
    # Pas de service publié, seulement un brouillon
    make_service(structure=structure, status=ServiceStatus.DRAFT)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) not in structure_ids


def test_structure_without_services_and_without_member_is_excluded(
    authenticated_user, api_client
):
    """Structure sans aucun service et sans membre réel est exclue"""
    structure = make_structure(user=None)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) not in structure_ids


def test_obsolete_structure_with_published_service_is_excluded(
    authenticated_user, api_client
):
    """Structure obsolète avec service publié est exclue"""
    structure = make_structure(user=None, is_obsolete=True)
    make_service(structure=structure, status=ServiceStatus.PUBLISHED)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) not in structure_ids


def test_obsolete_structure_with_member_is_excluded(authenticated_user, api_client):
    """Structure obsolète avec membre réel est exclue"""
    user = make_user()
    structure = make_structure(user=user, is_obsolete=True)

    response = api_client.get("/api/v2/structures/")

    assert 200 == response.status_code
    structure_ids = [s["id"] for s in response.data]
    assert str(structure.id) not in structure_ids


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
        StructureNationalLabel.objects.get(value="cnaf"),
        StructureNationalLabel.objects.get(value="afpa"),
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
    data = response.json()
    assert sorted(data["labels_nationaux"]) == ["afpa", "cnaf"]
    assert data == {
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
        "labels_nationaux": sorted(data["labels_nationaux"]),
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
    baker.make(Department, code="29", name="Finistère", region="53")
    baker.make(
        City,
        code="29188",
        name="Plougasnou",
        department="29",
        epci="",
        region="53",
        center=Point(3.8, 48.7, srid=WGS84),
    )

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
        modes_mobilisation=[
            ModeMobilisation.ENVOYER_UN_COURRIEL,
            ModeMobilisation.FORMULAIRE_DORA,
        ],
        mobilisable_par=[
            PersonneMobilisatrice.USAGERS,
            PersonneMobilisatrice.PROFESSIONNELS,
        ],
        mobilisation_precisions="Contacter conseiller(e) Pôle Emploi",
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
    service.location_kinds.add(
        LocationKind.objects.get(value=ModeAccueil.EN_PRESENTIEL)
    )
    service.location_kinds.add(LocationKind.objects.get(value=ModeAccueil.A_DISTANCE))
    service.requirements.add(
        baker.make(Requirement, name="Bonne connaissance du français oral et écrit"),
    )
    service.credentials.add(
        baker.make(Credential, name="Carte d'identité, passeport ou permis de séjour"),
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 200 == response.status_code
    data = response.json()
    expected = {
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
        # "formulaire-dora" n'existe pas dans le schéma data·inclusion : il est
        # exposé comme un lien de mobilisation vers le formulaire DORA
        "modes_mobilisation": [
            "envoyer-un-courriel",
            "utiliser-lien-mobilisation",
        ],
        "mobilisable_par": ["usagers", "professionnels"],
        "mobilisation_precisions": "Contacter conseiller(e) Pôle Emploi",
        "lien_mobilisation": service.get_dora_form_url(),
    }
    # Compare with order-independent list fields
    for key in ("modes_accueil", "modes_mobilisation"):
        assert sorted(data[key]) == sorted(expected[key])
    for key, expected_val in expected.items():
        if key not in ("modes_accueil", "modes_mobilisation"):
            assert data[key] == expected_val


def test_service_publics_export_empty_maps_to_tous_publics(
    authenticated_user, api_client
):
    service = make_service(status=ServiceStatus.PUBLISHED)
    service.publics.clear()  # no publics

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert response.status_code == 200
    assert response.json()["publics"] == ["tous-publics"]


def test_service_publics_export_all_maps_to_tous_publics(
    authenticated_user, api_client
):
    all_real_publics = [p.value for p in DiPublic if p != DiPublic.TOUS_PUBLICS]
    service = make_service(status=ServiceStatus.PUBLISHED)
    service.publics.clear()
    service.publics.add(
        baker.make(Public, name="tous", corresponding_di_publics=all_real_publics)
    )  # all publics

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert response.status_code == 200
    assert response.json()["publics"] == ["tous-publics"]


def test_service_serialization_formulaire_en_ligne(
    authenticated_user, api_client, settings
):
    # Initialisation du service
    service = make_service(status=ServiceStatus.PUBLISHED)
    service.modes_mobilisation = [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION,
        ModeMobilisation.FORMULAIRE_DORA,
    ]
    service.lien_mobilisation = "http://example.com/mobilisation-form"
    service.online_form = "http://example.com/online-form"
    service.save()

    # Formulaire en ligne = lien de mobilisation du service
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] == "http://example.com/mobilisation-form"

    # Formulaire en ligne = formulaire DORA
    service.modes_mobilisation = [ModeMobilisation.FORMULAIRE_DORA]
    service.lien_mobilisation = ""
    service.save()
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    json = response.json()
    assert json["formulaire_en_ligne"] == service.get_dora_form_url()

    # Formulaire en ligne = lien documents : un lien de mobilisation orphelin,
    # sans son mode, n'est pas exposé et ne masque pas le formulaire en ligne
    service.modes_mobilisation = [ModeMobilisation.TELEPHONER]
    service.lien_mobilisation = "http://example.com/mobilisation-form"
    service.save()
    response = api_client.get(f"/api/v2/services/{service.id}/")
    assert response.status_code == 200
    assert response.json()["lien_mobilisation"] is None

    service.lien_mobilisation = ""
    service.save()
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


def test_service_serialization_lien_mobilisation_mode_without_link(
    authenticated_user, api_client
):
    # Le mode ne peut pas être exposé sans son lien : le schéma data·inclusion
    # attend les deux ensemble.
    service = make_service(status=ServiceStatus.PUBLISHED)
    service.modes_mobilisation = [
        ModeMobilisation.TELEPHONER,
        ModeMobilisation.UTILISER_LIEN_MOBILISATION,
    ]
    service.lien_mobilisation = ""
    service.save()

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert response.status_code == 200
    json = response.json()
    assert json["modes_mobilisation"] == ["telephoner"]
    assert json["lien_mobilisation"] is None


def test_service_serialization_exemple_need_di_user(api_client):
    baker.make(Department, code="29", name="Finistère", region="53")
    baker.make(
        City,
        code="29188",
        name="Plougasnou",
        department="29",
        epci="",
        region="53",
        center=Point(3.8, 48.7, srid=WGS84),
    )

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
    service.location_kinds.add(
        LocationKind.objects.get(value=ModeAccueil.EN_PRESENTIEL)
    )
    service.location_kinds.add(LocationKind.objects.get(value=ModeAccueil.A_DISTANCE))
    service.requirements.add(
        baker.make(Requirement, name="Bonne connaissance du français oral et écrit"),
    )
    service.credentials.add(
        baker.make(Credential, name="Carte d'identité, passeport ou permis de séjour"),
    )

    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert 401 == response.status_code


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


def test_service_includes_contact_info_even_when_not_public(
    authenticated_user, api_client
):
    service = make_service(
        is_contact_info_public=False,
        status=ServiceStatus.PUBLISHED,
        contact_email="private@email.com",
        contact_phone="0123456789",
        contact_name="Test Person",
    )
    response = api_client.get(f"/api/v2/services/{service.id}/")

    assert response.status_code == 200

    assert response.data["courriel"] == "private@email.com"
    assert response.data["telephone"] == "0123456789"
    assert response.data["contact_nom_prenom"] == "Test Person"
    assert response.data["contact_public"] is False
