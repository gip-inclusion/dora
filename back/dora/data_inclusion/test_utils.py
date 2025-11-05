from typing import Optional
from uuid import uuid4


def make_di_service_data(**kwargs) -> dict:
    source = kwargs.pop("source", "emplois-de-linclusion")
    structure_id = f"{source}--{str(uuid4())}"
    return {
        **{
            "_di_geocodage_code_insee": None,
            "_di_geocodage_score": None,
            "source": source,
            "structure_id": structure_id,
            "id": f"{source}--{str(uuid4())}",
            "nom": "Atelier insertion et posture professionnelle",
            "description": "Cet atelier-conseil vous permet d’identifier les compétences à développer pour atteindre vos objectifs d’évolution professionnelle et à découvrir les différentes modalités de formation.  Durée d’une journée et inscription via votre espace France Travail.",
            "lien_source": "https://dora.inclusion.beta.gouv.fr/services/ass-pour-droit-a-l-i-nhes",
            "date_maj": "2025-02-14",
            "type": "accompagnement",
            "thematiques": ["numerique--acquerir-un-equipement"],
            "frais": "gratuit",
            "frais_precisions": "10€ pour l’adhésion annuelle",
            "publics": ["femmes"],
            "publics_precisions": "Le jeune entre 15 et 18 ans.",
            "conditions_acces": "Maîtrise de la langue française à l’oral et à l’écrit",
            "commune": "string",
            "code_postal": "60105",
            "code_insee": "ZDHwi",
            "adresse": "string",
            "complement_adresse": "string",
            "longitude": 0,
            "latitude": 0,
            "telephone": "+33123456789",
            "courriel": "exemple@inclusion.gouv.fr",
            "modes_accueil": ["a-distance"],
            "zone_eligibilite": ["75056"],
            "contact_nom_prenom": "string",
            "lien_mobilisation": "https://www.actionlogement.fr/demande-cfi",
            "modes_mobilisation": ["envoyer-un-courriel"],
            "mobilisable_par": ["professionnels"],
            "mobilisation_precisions": "La demande est à faire depuis l’espace personnel du demandeur d’emploi, rubrique « mes aides », formulaire spécifique « Aide à la mobilité ».",
            "volume_horaire_hebdomadaire": 1,
            "nombre_semaines": 3,
            "horaires_accueil": "Mo-Fr 08:30-12:30; PH off",
            "score_qualite": 1,
            "structure": {
                "source": source,
                "id": structure_id,
                "nom": "Centre social Le Tournesol",
                "date_maj": "2025-02-14",
                "description": "L’association 3027 offre un accès gratuit aux arts, à la culture et au sport pour toutes et tous sans distinction et en priorité aux personnes en situation de précarité et d’isolement.",
                "lien_source": "https://dora.inclusion.beta.gouv.fr/structures/ass-pour-droit-a-l-i-nhes",
                "siret": "13003013300016",
                "commune": "string",
                "code_postal": "10298",
                "code_insee": "w45i9",
                "adresse": "string",
                "complement_adresse": "string",
                "longitude": 0,
                "latitude": 0,
                "telephone": "+33123456789",
                "courriel": "exemple@inclusion.gouv.fr",
                "site_web": "https://example.com/",
                "horaires_accueil": "Mo-Fr 08:30-12:30; PH off",
                "accessibilite_lieu": "https://acceslibre.beta.gouv.fr/app/17-la-greve-sur-mignon/a/mairie/erp/mairie-la-greve-sur-mignon/",
                "reseaux_porteurs": ["mission-locale"],
            },
        },
        **kwargs,
    }


class FakeDataInclusionClient:
    """This is a fake data.inclusion client.

    It fakes an in-memory data.inclusion backend, leveraging ducktyping of
    the actual ``DataInclusionClient`` implementation.

    The goal of this client is not be fully compliant with the real behaviour,
    but to merely impersonate it, to be able to do assertions about the calling
    code.

    The fake client is injected during tests to the views that depends on the
    data.inclusion backend.
    """

    def __init__(self, services: Optional[list[dict]] = None) -> None:
        self.services = services if services is not None else []

    def list_services(self, source: Optional[str] = None) -> Optional[list[dict]]:
        raise NotImplementedError()

    def retrieve_service(
        self,
        id: str,
        user_agent: Optional[str] = None,
        user_hash: Optional[str] = None,
    ) -> Optional[dict]:
        return next((s for s in self.services if s["id"] == id), None)

    def search_services(
        self,
        sources: Optional[str] = None,
        score_qualite_minimum: Optional[float] = None,
        code_insee: Optional[str] = None,
        thematiques: Optional[list[str]] = None,
        types: Optional[list[str]] = None,
        frais: Optional[list[str]] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> Optional[list[dict]]:
        services = self.services

        if sources is not None:
            services = [r for r in services if r["source"] in sources]

        if score_qualite_minimum is not None:
            services = [
                r for r in services if r["score_qualite"] >= score_qualite_minimum
            ]

        if thematiques is not None:
            services = [
                r
                for r in services
                if any(
                    t.startswith(requested_thematique)
                    for t in r["thematiques"]
                    for requested_thematique in thematiques
                )
            ]

        if types is not None:
            services = [r for r in services if any(t in r["types"] for t in types)]

        if frais is not None:
            services = [r for r in services if any(t in r["frais"] for t in frais)]

        if code_insee is not None:
            # filter for zone_diffusion_type=commune only
            # the goal is simply to make it possible to
            # validate the usage of the zone_diffusion_* by the caller
            services = [
                r
                for r in services
                if r["zone_diffusion_type"] != "commune"
                or r["zone_diffusion_code"] == code_insee
            ]

            return [
                # overly simple distance for tests.
                {
                    "distance": 30 if code_insee != s["code_insee"] else 0,
                    "service": s,
                }
                for s in services
            ]
        else:
            return [{"distance": 30, "service": s} for s in services]
