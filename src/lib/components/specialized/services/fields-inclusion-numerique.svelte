<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/inputs/checkboxes-field.svelte";
  import MultiSelectField from "$lib/components/inputs/multi-select-field.svelte";
  import SelectField from "$lib/components/inputs/select-field.svelte";
  import TextareaField from "$lib/components/inputs/textarea-field.svelte";
  import FieldsAddress from "$lib/components/specialized/services/fields-address.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsPerimeter from "$lib/components/specialized/services/fields-perimeter.svelte";
  import type { Choice, Service, ServicesOptions, Structure } from "$lib/types";
  import { moveToTheEnd, orderAndReformatSubcategories } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";
  import type { Schema } from "$lib/validation/schemas/utils";
  import { onMount } from "svelte";

  export let schema: Schema;
  export let servicesOptions: ServicesOptions;
  export let service: Service;
  export let structure: Structure;

  let subcategories = [];

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

  function updateServicePresentation(subcategories) {
    service.name = "Médiation numérique";
    service.shortDesc = `${
      structure.name
    } propose des services : ${subcategories.slice(
      0,
      253 - structure.name.length
    )}${subcategories.length > 253 - structure.name.length ? "…" : ""}`;
  }

  function setCategories(categories = ["numerique"]) {
    subcategories = servicesOptions.subcategories.filter(({ value }) =>
      categories.some(
        (cat) => value.startsWith(cat) && value !== "numerique--autre"
      )
    );

    subcategories = orderAndReformatSubcategories(
      subcategories,
      categories,
      servicesOptions
    );

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }

  service.locationKinds = [];

  function setModalites() {
    service.coachOrientationModes = ["autre"];
    service.coachOrientationModesOther =
      "Mêmes modalités que pour les bénéficiaires";
  }

  function setDiffusionZone() {
    if (!structure.latitude || !structure.longitude) return;
    service.diffusionZoneType = "department";
    service.diffusionZoneDetails = structure.department;
  }

  function setLocationKinds() {
    service.locationKinds = ["en-presentiel"];
  }

  function setContact() {
    if (structure.phone && !service.contactPhone) {
      service.contactPhone = structure.phone;
    }

    if (structure.email && !service.contactEmail) {
      service.contactEmail = structure.email;
    }
  }

  function setConcernedPublic() {
    service.concernedPublic = service.concernedPublic.filter(
      (concernedPublicValue: string): boolean =>
        concernedPublicOptions
          .map((concernedPublicOption): string => concernedPublicOption.value)
          .includes(concernedPublicValue)
    );
  }

  setCategories();
  setConcernedPublic();
  setContact();

  onMount(() => {
    setModalites();
    setDiffusionZone();
    setLocationKinds();
  });

  function handleSubcategoriesChange(subcategories) {
    updateServicePresentation(
      servicesOptions.subcategories
        .filter((subcategory) => subcategories.includes(subcategory.value))
        .map((subcategory) => subcategory.label)
        .join(", ")
    );
  }
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

  <MultiSelectField
    id="subcategories"
    schema={schema.subcategories}
    bind:value={service.subcategories}
    choices={subcategories}
    placeholder="Sélectionner"
    placeholderMulti="Sélectionner"
    onChange={handleSubcategoriesChange}
  />

  {#if concernedPublicOptions.length}
    <MultiSelectField
      id="concernedPublic"
      schema={schema.concernedPublic}
      bind:value={service.concernedPublic}
      choices={concernedPublicOptions}
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
    />
  {/if}

  {#if kindsOptions.length}
    <CheckboxesField
      id="kinds"
      schema={schema.kinds}
      bind:value={service.kinds}
      choices={kindsOptions}
      _notrequired
    />
  {/if}

  <SelectField
    id="feeCondition"
    schema={schema.feeCondition}
    placeholder="Choisissez…"
    bind:value={service.feeCondition}
    choices={servicesOptions.feeConditions}
  />

  {#if isNotFreeService(service.feeCondition)}
    <TextareaField
      id="feeDetails"
      schema={schema.feeDetails}
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
    schema={schema.beneficiariesAccessModes}
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
      schema={schema.beneficiariesAccessModesOther}
      hideLabel
      placeholder="Merci de préciser la modalité"
      bind:value={service.beneficiariesAccessModesOther}
    />
  {/if}
</FieldSet>

{#if !structure.latitude || !structure.longitude}
  <FieldsPerimeter bind:service {servicesOptions} {schema} />
{/if}

<FieldSet title="Accueil">
  <FieldsAddress bind:entity={service} parent={structure} {schema} />
</FieldSet>

<FieldsContact bind:service {schema} />
