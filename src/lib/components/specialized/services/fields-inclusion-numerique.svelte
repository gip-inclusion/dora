<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import FieldsAddress from "$lib/components/specialized/services/fields-address.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsPerimeter from "$lib/components/specialized/services/fields-perimeter.svelte";
  import type {
    Choice,
    Service,
    ServiceKind,
    ServicesOptions,
    ShortStructure,
    Structure,
  } from "$lib/types";
  import { moveToTheEnd } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";
  import FieldSubcategory from "./field-subcategory.svelte";

  export let servicesOptions: ServicesOptions;
  export let service: Service;
  export let structure: Structure | ShortStructure;

  function existInServicesOptionsConcernedPublic(concernedPublicOption) {
    return servicesOptions.concernedPublic
      .filter(
        (genericConcernedPublicOption): boolean =>
          genericConcernedPublicOption.structure == null
      )
      .map(
        (genericConcernedPublicOption: Choice): string =>
          genericConcernedPublicOption.label
      )
      .includes(concernedPublicOption.label);
  }

  function addServicesOptionsConcernedPublicValues(concernedPublicOption: {
    label: string;
  }): Choice {
    return {
      label: concernedPublicOption.label,
      value: servicesOptions.concernedPublic.find(
        (option: Choice) => option.label === concernedPublicOption.label
      ).value,
    };
  }

  const concernedPublicOptions: Choice[] = [
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
    .filter(existInServicesOptionsConcernedPublic)
    .map(addServicesOptionsConcernedPublicValues);

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

  function filterConcernedPublics() {
    service.concernedPublic = service.concernedPublic.filter(
      (concernedPublicValue: string): boolean =>
        concernedPublicOptions
          .map((concernedPublicOption): string => concernedPublicOption.value)
          .includes(concernedPublicValue)
    );
  }

  function filterKinds() {
    service.kinds = service.kinds.filter((kind: ServiceKind) =>
      kindsOptions.map((option) => option.value).includes(kind)
    );
  }

  service.locationKinds = [];
  filterConcernedPublics();
  preSetContact();
  preSetDiffusionZone();
  filterKinds();
</script>

<FieldSet title="Service de l'inclusion numérique">
  <div slot="help">
    <p class="text-f14">
      Le <b>Formulaire de l'inclusion numérique</b> est un outil de saisie
      compatible avec le
      <a
        href="https://lamednum.coop/schema-de-donnees-des-lieux-de-mediation-numerique-2/"
        target="_blank"
        rel="noreferrer"
        class="underline">schéma de données des lieux de médiation numérique</a
      >.
      <br />
      La standardisation des données de l'inclusion numérique permet de décrire l’offre
      disponible de manière harmonisée, assurant ainsi la compatibilité de ces données
      avec de nombreux outils.
    </p>
  </div>

  <FieldSubcategory bind:service {servicesOptions} />

  {#if concernedPublicOptions.length}
    <MultiSelectField
      id="concernedPublic"
      bind:value={service.concernedPublic}
      choices={concernedPublicOptions}
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
    />
  {/if}

  {#if kindsOptions.length}
    <CheckboxesField
      id="kinds"
      bind:value={service.kinds}
      choices={kindsOptions}
    />
  {/if}

  <RadioButtonsField
    id="feeCondition"
    bind:value={service.feeCondition}
    choices={servicesOptions.feeConditions}
  />

  {#if isNotFreeService(service.feeCondition)}
    <TextareaField
      id="feeDetails"
      placeholder="Merci de détailler ici les frais à charge du bénéficiaire : adhésion, frais de location, frais de garde, etc., et les montants."
      bind:value={service.feeDetails}
    />
  {/if}
</FieldSet>

<FieldSet title="Modalités">
  <div slot="help">
    <p class="text-f14">Modalités pour mobiliser le service.</p>
  </div>

  <CheckboxesField
    id="beneficiariesAccessModes"
    choices={moveToTheEnd(
      servicesOptions.beneficiariesAccessModes,
      "value",
      "autre"
    )}
    bind:value={service.beneficiariesAccessModes}
  />

  {#if service.beneficiariesAccessModes.includes("autre")}
    <BasicInputField
      id="beneficiariesAccessModesOther"
      hideLabel
      placeholder="Merci de préciser la modalité"
      bind:value={service.beneficiariesAccessModesOther}
    />
  {/if}
</FieldSet>

{#if !structure.department}
  <FieldsPerimeter bind:service {servicesOptions} />
{/if}

<FieldSet title="Accueil">
  <FieldsAddress bind:entity={service} parent={structure} />
</FieldSet>

<FieldsContact bind:service />
