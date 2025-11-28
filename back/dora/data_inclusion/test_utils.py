from typing import Optional
from uuid import uuid4


def make_di_service_data(**kwargs) -> dict:
    return {
        **{
            "_di_geocodage_code_insee": None,
            "_di_geocodage_score": None,
            "id": str(uuid4()),
            "structure_id": "rouge-empire",
            "source": "odspep",
            "nom": "Munoz",
            "presentation_resume": "Puissant fine.",
            "presentation_detail": "Épaule élever un.",
            "types": [],
            "thematiques": [],
            "prise_rdv": "https://teixeira.fr/",
            "frais": [],
            "frais_autres": "Camarade il.",
            "profils": ["femmes", "jeunes-16-26"],
            "pre_requis": [],
            "cumulable": False,
            "justificatifs": [],
            "formulaire_en_ligne": None,
            "commune": "Sainte Jacquelineboeuf",
            "code_postal": "25454",
            "code_insee": None,
            "adresse": "chemin de Ferreira",
            "complement_adresse": "2ème étage",
            "longitude": -61.64115,
            "latitude": 9.8741475,
            "recurrence": "Tous les jours de la semaine",
            "date_creation": "2022-01-01",
            "date_suspension": "2054-01-01",
            "lien_source": "https://dora.fr/cacher-violent",
            "telephone": "0102030405",
            "courriel": "xavierlaunay@example.org",
            "contact_info_filled": True,
            "contact_public": False,
            "contact_nom_prenom": "David Rocher",
            "date_maj": "2023-01-01",
            "modes_accueil": ["en-presentiel"],
            "modes_orientation_accompagnateur": ["telephoner", "autre"],
            "modes_orientation_accompagnateur_autres": "Mêmes modalités que pour les bénéficiaires",
            "modes_orientation_beneficiaire": ["telephoner", "autre"],
            "modes_orientation_beneficiaire_autres": "Contacter conseiller(e) Pôle Emploi",
            "score_qualite": 0.5,
            "zone_diffusion_type": None,
            "zone_diffusion_code": None,
            "zone_diffusion_nom": "foo",
            "structure": {
                "nom": "Rouge Empire",
                "commune": "Sainte Jacquelineboeuf",
                "code_insee": "59999",
                "telephone": "1234",
                "courriel": "contact@example.com",
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
        source: str,
        id: str,
        user_agent: Optional[str] = None,
        user_hash: Optional[str] = None,
    ) -> Optional[dict]:
        return next(
            (s for s in self.services if s["source"] == source and s["id"] == id), None
        )

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
