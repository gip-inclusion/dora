<script lang="ts">
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import HiddenField from "$lib/components/inputs/hidden-field.svelte";
  import MultiSelectField from "$lib/components/inputs/multi-select-field.svelte";
  import OpeningHoursField from "$lib/components/inputs/opening-hours-field.svelte";
  import RichTextField from "$lib/components/inputs/rich-text-field.svelte";
  import SelectField from "$lib/components/inputs/select-field.svelte";
  import TextareaField from "$lib/components/inputs/textarea-field.svelte";
  import FieldsAddress from "$lib/components/specialized/services/fields-address.svelte";
  import type { Structure, StructuresOptions } from "$lib/types";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
  import { structureSchema } from "$lib/validation/schemas/structure";

  export let structure: Structure;
  export let structuresOptions: StructuresOptions;

  function getAccessLibreUrl(structure: Structure) {
    const department = getDepartmentFromCityCode(structure.cityCode);
    const where = encodeURIComponent(`${structure.city} (${department})`);
    const lat = encodeURIComponent(structure.latitude);
    const long = encodeURIComponent(structure.longitude);
    const code = encodeURIComponent(structure.cityCode);
    return `https://acceslibre.beta.gouv.fr/recherche/?what=&where=${where}&lat=${lat}&lon=${long}&code=${code}`;
  }

  $: accesslibreUrl = getAccessLibreUrl(structure);
</script>

<BasicInputField
  id="siret"
  schema={structureSchema.siret}
  bind:value={structure.siret}
/>

<BasicInputField
  id="name"
  schema={structureSchema.name}
  bind:value={structure.name}
  placeholder="Plateforme de l’inclusion"
/>

<SelectField
  id="typology"
  schema={structureSchema.typology}
  bind:value={structure.typology}
  choices={structuresOptions.typologies}
  placeholder="Choisissez…"
  sort
/>

<FieldsAddress bind:entity={structure} schema={structureSchema} />

<BasicInputField
  type="url"
  id="accesslibreUrl"
  schema={structureSchema.accesslibreUrl}
  bind:value={structure.accesslibreUrl}
  placeholder="https://acceslibre.beta.gouv.fr/…"
  vertical
>
  <div slot="description">
    <small>
      Afin de renseigner les informations d’accessibilité sur la structure,
      retrouvez-la via la plateforme
      <a
        class="text-magenta-cta underline"
        href={accesslibreUrl}
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener noreferrer">acceslibre</a
      >
      et copiez l’url dans le champ ci-dessous.
    </small>
  </div>
</BasicInputField>

<BasicInputField
  type="tel"
  id="phone"
  schema={structureSchema.phone}
  bind:value={structure.phone}
  placeholder="0X XX XX XX XX"
/>

<BasicInputField
  type="email"
  id="email"
  schema={structureSchema.email}
  bind:value={structure.email}
  placeholder="nom.prenom@organisation.fr"
/>

<BasicInputField
  type="url"
  id="url"
  schema={structureSchema.url}
  bind:value={structure.url}
  placeholder="https://mastructure.fr"
/>

<TextareaField
  id="shortDesc"
  schema={structureSchema.shortDesc}
  bind:value={structure.shortDesc}
  placeholder="Décrivez brièvement votre structure"
/>

<RichTextField
  id="fullDesc"
  schema={structureSchema.fullDesc}
  bind:value={structure.fullDesc}
  placeholder="Présentation détaillée de la structure"
  vertical
/>

<MultiSelectField
  id="nationalLabels"
  schema={structureSchema.nationalLabels}
  bind:value={structure.nationalLabels}
  choices={structuresOptions.nationalLabels}
  description="Indiquez si la structure fait partie d'un ou plusieurs réseaux nationaux"
  placeholder="Choisissez…"
  placeholderMulti="Choisissez…"
  vertical
/>

<BasicInputField
  id="otherLabels"
  schema={structureSchema.otherLabels}
  bind:value={structure.otherLabels}
  description="Indiquez si la structure fait partie d’autres labels (régionaux, locaux…)"
  vertical
/>

<OpeningHoursField
  id="openingHours"
  schema={structureSchema.openingHours}
  bind:value={structure.openingHours}
  vertical
/>

<BasicInputField
  id="openingHoursDetails"
  schema={structureSchema.openingHoursDetails}
  bind:value={structure.openingHoursDetails}
  description="Vous pouvez renseigner des informations spécifiques concernant les horaires dans ce champ"
  vertical
/>

<HiddenField id="ape" schema={structureSchema.ape} bind:value={structure.ape} />
