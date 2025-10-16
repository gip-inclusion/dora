from django.conf import settings

# from django.core.files.storage import default_storage
from rest_framework import serializers

from dora.services.models import (
    Service,
)
from dora.structures.models import Structure

############
# V2
############


class StructureSerializer(serializers.ModelSerializer):
    accessibilite = serializers.SerializerMethodField()
    adresse = serializers.SerializerMethodField()
    antenne = serializers.SerializerMethodField()
    code_insee = serializers.SerializerMethodField()
    code_postal = serializers.SerializerMethodField()
    commune = serializers.SerializerMethodField()
    complement_adresse = serializers.SerializerMethodField()
    courriel = serializers.SerializerMethodField()
    date_maj = serializers.SerializerMethodField()
    horaires_ouverture = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    labels_autres = serializers.SerializerMethodField()
    labels_nationaux = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    lien_source = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    nom = serializers.SerializerMethodField()
    presentation_detail = serializers.SerializerMethodField()
    presentation_resume = serializers.SerializerMethodField()
    rna = serializers.SerializerMethodField()
    siret = serializers.SerializerMethodField()
    siret = serializers.SerializerMethodField()
    parent_siret = serializers.SerializerMethodField()
    site_web = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    telephone = serializers.SerializerMethodField()
    thematiques = serializers.SerializerMethodField()
    typologie = serializers.SerializerMethodField()

    class Meta:
        model = Structure

        fields = [
            "accessibilite",
            "adresse",
            "antenne",
            "code_insee",
            "code_postal",
            "commune",
            "complement_adresse",
            "courriel",
            "date_maj",
            "horaires_ouverture",
            "id",
            "labels_autres",
            "labels_nationaux",
            "latitude",
            "lien_source",
            "longitude",
            "nom",
            "presentation_detail",
            "presentation_resume",
            "rna",
            "siret",
            "parent_siret",
            "site_web",
            "source",
            "telephone",
            "thematiques",
            "typologie",
        ]

    def get_accessibilite(self, obj):
        return obj.accesslibre_url or None

    def get_adresse(self, obj):
        return obj.address1 or None

    def get_antenne(self, obj) -> bool:
        return obj.parent_id is not None

    def get_code_insee(self, obj):
        return obj.city_code or None

    def get_code_postal(self, obj):
        return obj.postal_code or None

    def get_commune(self, obj):
        return obj.city or None

    def get_complement_adresse(self, obj):
        return obj.address2 or None

    def get_courriel(self, obj):
        return obj.email or None

    def get_date_maj(self, obj):
        return obj.modification_date or None

    def get_horaires_ouverture(self, obj) -> str:
        oh = obj.opening_hours
        dets = obj.opening_hours_details
        if oh:
            if dets:
                return f'{oh}; "{dets}"'
            return oh
        elif dets:
            return f'"{dets}"'
        return None

    def get_id(self, obj):
        return str(obj.id)

    def get_labels_autres(self, obj):
        return obj.other_labels

    def get_labels_nationaux(self, obj):
        return [label.value for label in obj.national_labels.all()]

    def get_latitude(self, obj):
        return obj.latitude

    def get_lien_source(self, obj) -> str:
        return obj.get_frontend_url()

    def get_longitude(self, obj):
        return obj.longitude

    def get_nom(self, obj):
        return obj.name or None

    def get_presentation_detail(self, obj):
        return obj.full_desc or None

    def get_presentation_resume(self, obj):
        return obj.short_desc or None

    def get_rna(self, obj):
        return None

    def get_siret(self, obj):
        return obj.siret or None

    def get_parent_siret(self, obj) -> str:
        return obj.parent.siret if obj.parent else None

    def get_site_web(self, obj):
        return obj.url or None

    def get_source(self, obj):
        return obj.source.value if obj.source else None

    def get_telephone(self, obj):
        return obj.phone or None

    def get_thematiques(self, obj):
        # Les thématiques sont portées par les services
        return None

    def get_typologie(self, obj):
        return obj.typology


class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    structure_id = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    nom = serializers.SerializerMethodField()
    presentation_resume = serializers.SerializerMethodField()
    presentation_detail = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    thematiques = serializers.SerializerMethodField()
    prise_rdv = serializers.SerializerMethodField()
    frais = serializers.SerializerMethodField()
    frais_autres = serializers.SerializerMethodField()
    profils = serializers.SerializerMethodField()
    publics = serializers.SerializerMethodField()
    publics_precisions = serializers.SerializerMethodField()
    pre_requis = serializers.SerializerMethodField()
    cumulable = serializers.SerializerMethodField()
    justificatifs = serializers.SerializerMethodField()
    formulaire_en_ligne = serializers.SerializerMethodField()
    commune = serializers.SerializerMethodField()
    code_postal = serializers.SerializerMethodField()
    code_insee = serializers.SerializerMethodField()
    adresse = serializers.SerializerMethodField()
    complement_adresse = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    recurrence = serializers.SerializerMethodField()
    date_creation = serializers.SerializerMethodField()
    date_maj = serializers.SerializerMethodField()
    date_suspension = serializers.SerializerMethodField()
    lien_source = serializers.SerializerMethodField()
    telephone = serializers.SerializerMethodField()
    courriel = serializers.SerializerMethodField()
    contact_nom_prenom = serializers.SerializerMethodField()
    contact_public = serializers.SerializerMethodField()
    modes_accueil = serializers.SerializerMethodField()
    zone_diffusion_type = serializers.SerializerMethodField()
    zone_diffusion_code = serializers.SerializerMethodField()
    zone_diffusion_nom = serializers.SerializerMethodField()
    modes_orientation_accompagnateur = serializers.SerializerMethodField()
    modes_orientation_accompagnateur_autres = serializers.SerializerMethodField()
    modes_orientation_beneficiaire = serializers.SerializerMethodField()
    modes_orientation_beneficiaire_autres = serializers.SerializerMethodField()
    temps_passe_duree_hebdomadaire = serializers.SerializerMethodField()
    temps_passe_semaines = serializers.SerializerMethodField()

    class Meta:
        model = Service

        fields = [
            "adresse",
            "code_insee",
            "code_postal",
            "commune",
            "complement_adresse",
            "contact_nom_prenom",
            "contact_public",
            "courriel",
            "cumulable",
            "date_creation",
            "date_maj",
            "date_suspension",
            "formulaire_en_ligne",
            "frais_autres",
            "frais",
            "id",
            "justificatifs",
            "latitude",
            "lien_source",
            "longitude",
            "modes_accueil",
            "nom",
            "pre_requis",
            "presentation_detail",
            "presentation_resume",
            "prise_rdv",
            "profils",
            "publics",
            "publics_precisions",
            "recurrence",
            "source",
            "structure_id",
            "telephone",
            "thematiques",
            "types",
            "zone_diffusion_code",
            "zone_diffusion_nom",
            "zone_diffusion_type",
            "modes_orientation_accompagnateur",
            "modes_orientation_accompagnateur_autres",
            "modes_orientation_beneficiaire",
            "modes_orientation_beneficiaire_autres",
            "temps_passe_duree_hebdomadaire",
            "temps_passe_semaines",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def get_structure_id(self, obj):
        return str(obj.structure_id)

    def get_source(self, obj):
        return obj.source.value if obj.source else None

    def get_nom(self, obj):
        return obj.name

    def get_presentation_resume(self, obj):
        return obj.short_desc or None

    def get_presentation_detail(self, obj):
        return obj.full_desc or None

    def get_types(self, obj):
        return [k.value for k in obj.kinds.all()]

    def get_thematiques(self, obj):
        scats = [scat.value for scat in obj.subcategories.all()]
        return [scat for scat in scats if not scat.endswith("--autre")]

    def get_prise_rdv(self, obj):
        return obj.appointment_link

    def get_frais(self, obj):
        return obj.fee_condition.value if obj.fee_condition else None

    def get_frais_autres(self, obj):
        return obj.fee_details or None

    def get_profils(self, obj):
        return [c.name for c in obj.publics.all()]

    def get_publics(self, obj):
        all_items = [
            item
            for public in obj.publics.all()
            for item in public.corresponding_di_publics
        ]
        return list(dict.fromkeys(all_items))

    def get_publics_precisions(self, obj):
        return ", ".join([p.name for p in obj.publics.all()])

    def get_pre_requis(self, obj):
        return [c.name for c in obj.requirements.all()]

    def get_cumulable(self, obj):
        return obj.is_cumulative

    def get_justificatifs(self, obj):
        return [c.name for c in obj.credentials.all()]

    def get_formulaire_en_ligne(self, obj):
        coach_orientation_mode_values = set(
            m.value for m in obj.coach_orientation_modes.all()
        )
        beneficiaries_access_mode_values = set(
            m.value for m in obj.beneficiaries_access_modes.all()
        )
        if "completer-le-formulaire-dadhesion" in coach_orientation_mode_values:
            return obj.coach_orientation_modes_external_form_link
        elif "completer-le-formulaire-dadhesion" in beneficiaries_access_mode_values:
            return obj.beneficiaries_access_modes_external_form_link
        elif "formulaire-dora" in coach_orientation_mode_values:
            return obj.get_dora_form_url()
        return obj.online_form if obj.online_form else None

    def get_commune(self, obj):
        return obj.city if obj.city else None

    def get_code_postal(self, obj):
        return obj.postal_code if obj.postal_code else None

    def get_code_insee(self, obj):
        return obj.city_code if obj.city_code else None

    def get_adresse(self, obj):
        return obj.address1 if obj.address1 else None

    def get_complement_adresse(self, obj):
        return obj.address2 if obj.address2 else None

    def get_longitude(self, obj):
        return obj.geom.x if obj.geom else None

    def get_latitude(self, obj):
        return obj.geom.y if obj.geom else None

    def get_recurrence(self, obj):
        return obj.recurrence if obj.recurrence else None

    def get_date_creation(self, obj):
        return obj.publication_date if obj.publication_date else None

    def get_date_maj(self, obj):
        return obj.modification_date or None

    def get_date_suspension(self, obj):
        return obj.suspension_date if obj.suspension_date else None

    def get_lien_source(self, obj):
        return obj.get_frontend_url()

    def get_telephone(self, obj):
        assert self.context.get("request").user.email == settings.DATA_INCLUSION_EMAIL
        return obj.contact_phone

    def get_courriel(self, obj):
        assert self.context.get("request").user.email == settings.DATA_INCLUSION_EMAIL
        return obj.contact_email

    def get_contact_nom_prenom(self, obj):
        assert self.context.get("request").user.email == settings.DATA_INCLUSION_EMAIL
        return obj.contact_name

    def get_contact_public(self, obj):
        return obj.is_contact_info_public

    def get_modes_accueil(self, obj):
        return [k.value for k in obj.location_kinds.all()]

    def get_zone_diffusion_type(self, obj):
        if obj.diffusion_zone_type == "city":
            return "commune"
        if obj.diffusion_zone_type == "epci":
            return "epci"
        if obj.diffusion_zone_type == "department":
            return "departement"
        if obj.diffusion_zone_type == "region":
            return "region"
        if obj.diffusion_zone_type == "country":
            return "pays"

    def get_zone_diffusion_code(self, obj):
        return obj.diffusion_zone_details

    def get_zone_diffusion_nom(self, obj):
        return obj.get_diffusion_zone_details_display()

    def get_modes_orientation_accompagnateur(self, obj):
        mapping = {
            # "formulaire-dora" n'est pas une valeur valide pour DI,
            # on la remplace donc par "completer-le-formulaire-dadhesion"
            "formulaire-dora": "completer-le-formulaire-dadhesion",
        }
        return [
            mapping.get(mode.value, mode.value)
            for mode in obj.coach_orientation_modes.all()
        ]

    def get_modes_orientation_accompagnateur_autres(self, obj):
        return obj.coach_orientation_modes_other

    def get_modes_orientation_beneficiaire(self, obj):
        # Pas de mapping nécessaire
        return [m.value for m in obj.beneficiaries_access_modes.all()]

    def get_modes_orientation_beneficiaire_autres(self, obj):
        return obj.beneficiaries_access_modes_other

    def get_temps_passe_duree_hebdomadaire(self, obj):
        return obj.duration_weekly_hours

    def get_temps_passe_semaines(self, obj):
        return obj.duration_weeks
