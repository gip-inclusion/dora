<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsAddress from "$lib/components/specialized/services/fields-address.svelte";
  import FieldsPerimeter from "../_common/fields-perimeter.svelte";
  import type {
    Choice,
    Service,
    ServiceKind,
    ServicesOptions,
    ShortStructure,
    Structure,
  } from "$lib/types";
  import { isNotFreeService } from "$lib/utils/service";
  import FieldSubcategory from "$lib/components/specialized/services/field-subcategory.svelte";

  import FieldsModalitiesBeneficiary from "./fields-modalities-beneficiary.svelte";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    structure: Structure | ShortStructure;
  }

  let { servicesOptions, service = $bindable(), structure }: Props = $props();

  function existInServicesOptionsPublics(publicsOption) {
    return servicesOptions.publics
      .filter(
        (genericPublicsOption): boolean =>
          genericPublicsOption.structure == null
      )
      .map((genericPublicsOption: Choice): string => genericPublicsOption.label)
      .includes(publicsOption.label);
  }

  function addServicesOptionsPublicsValues(publicsOption: {
    label: string;
  }): Choice {
    return {
      label: publicsOption.label,
      value: servicesOptions.publics.find(
        (option: Choice) => option.label === publicsOption.label
      ).value,
    };
  }

  const publicsOptions: Choice[] = [
    {
      label: "Familles/enfants",
      structure: null,
    },
    {
      label: "Jeunes (16-26 ans)",
      structure: null,
    },
    {
      label: "Adultes",
      structure: null,
    },
    {
      label: "Femmes",
      structure: null,
    },
    {
      label: "Seniors (+65 ans)",
      structure: null,
    },
    {
      label: "Publics langues étrangères",
      structure: null,
    },
    {
      label: "Déficience visuelle",
      structure: null,
    },
    {
      label: "Surdité",
      structure: null,
    },
    {
      label:
        "Handicaps psychiques : troubles psychiatriques donnant lieu à des atteintes comportementales",
      structure: null,
    },
    {
      label:
        "Handicaps mentaux : déficiences limitant les activités d’une personne",
      structure: null,
    },
    {
      label: "Personnes en situation d’illettrisme",
      structure: null,
    },
  ]
    .filter(existInServicesOptionsPublics)
    .map(addServicesOptionsPublicsValues);

  function existInServicesOptionsKinds(kindsOption) {
    return servicesOptions.kinds
      .map((genericKindsOption: Choice): string => genericKindsOption.value)
      .includes(kindsOption.value);
  }

  const kindsOptions = [
    {
      value: "autonomie",
      label: "Seul : j’ai accès à du matériel et une connexion",
    },
    {
      value: "accompagnement",
      label:
        "Avec de l’aide : je suis accompagné seul dans l’usage du numérique",
    },
    {
      value: "atelier",
      label:
        "Dans un atelier : j’apprends collectivement à utiliser le numérique",
    },
    {
      value: "delegation",
      label:
        "À ma place : une personne habilitée fait les démarches à ma place",
    },
  ].filter(existInServicesOptionsKinds);

  function preSetContact() {
    if (structure.phone && !service.contactPhone) {
      service.contactPhone = structure.phone;
    }

    if (structure.email && !service.contactEmail) {
      service.contactEmail = structure.email;
    }
  }

  function preSetDiffusionZone() {
    if (structure.department) {
      service.diffusionZoneType = "department";
      service.diffusionZoneDetails = structure.department;
    }
  }

  function filterPublics() {
    service.publics = service.publics.filter((publicsValue: string): boolean =>
      publicsOptions
        .map((publicsOption): string => publicsOption.value)
        .includes(publicsValue)
    );
  }

  function filterKinds() {
    service.kinds = service.kinds.filter((kind: ServiceKind) =>
      kindsOptions.map((option) => option.value).includes(kind)
    );
  }

  filterPublics();
  preSetContact();
  preSetDiffusionZone();
  filterKinds();
</script>

<FieldSet title="Service de l’inclusion numérique">
  {#snippet help()}
    <div>
      <p class="text-f14">
        Le <b>Formulaire de l’inclusion numérique</b> est un outil de saisie
        compatible avec le
        <a
          href="https://lamednum.coop/schema-de-donnees-des-lieux-de-mediation-numerique-2/"
          target="_blank"
          rel="noopener"
          class="underline"
          >schéma de données des lieux de médiation numérique</a
        >.
        <br />
        La standardisation des données de l’inclusion numérique permet de décrire
        l’offre disponible de manière harmonisée, assurant ainsi la compatibilité
        de ces données avec de nombreux outils.
      </p>
    </div>
  {/snippet}

  <FieldSubcategory
    bind:service
    {servicesOptions}
    description="Sélectionnez au moins un besoin."
  />

  {#if publicsOptions.length}
    <MultiSelectField
      id="publics"
      bind:value={service.publics}
      choices={publicsOptions}
      description="Si le service n’est pas ouvert à tous les publics, sélectionnez le profil concerné. Plusieurs choix possibles."
    />
  {/if}

  {#if kindsOptions.length}
    <CheckboxesField
      id="kinds"
      bind:value={service.kinds}
      choices={kindsOptions}
      description="Sélectionnez au moins une typologie de service. Plusieurs choix possibles."
    />
  {/if}

  <RadioButtonsField
    id="feeCondition"
    bind:value={service.feeCondition}
    choices={servicesOptions.feeConditions}
    description="Précisez si le service est gratuit ou payant pour les bénéficiaires."
  />

  {#if isNotFreeService(service.feeCondition)}
    <TextareaField
      id="feeDetails"
      description="Détaillez les frais à la charge des bénéficiaires, y compris leurs montants."
      bind:value={service.feeDetails}
    />
  {/if}
</FieldSet>

<FieldSet title="Modalités">
  {#snippet help()}
    <div>
      <p class="text-f14">Modalités pour mobiliser le service.</p>
    </div>
  {/snippet}

  <FieldsModalitiesBeneficiary
    id="beneficiariesAccessModes"
    {service}
    {servicesOptions}
  />
</FieldSet>

{#if !structure.department}
  <FieldsPerimeter bind:service {servicesOptions} />
{/if}

<FieldSet title="Accueil">
  <FieldsAddress bind:entity={service} parent={structure} />
</FieldSet>

<FieldsContact bind:service />
