<script lang="ts">
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import HiddenField from "$lib/components/forms/fields/hidden-field.svelte";
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import OpeningHoursField from "$lib/components/forms/fields/opening-hours-field.svelte";
  import RichTextField from "$lib/components/forms/fields/rich-text-field.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import FieldsAddress from "$lib/components/specialized/services/fields-address.svelte";
  import type { Structure, StructuresOptions } from "$lib/types";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";

  export let structure: Structure;
  export let structuresOptions: StructuresOptions;

  function getAccessLibreUrl(struct: Structure) {
    const department = getDepartmentFromCityCode(struct.cityCode);
    const where = encodeURIComponent(`${struct.city} (${department})`);
    const lat = encodeURIComponent(struct.latitude);
    const long = encodeURIComponent(struct.longitude);
    const code = encodeURIComponent(struct.cityCode);
    return `https://acceslibre.beta.gouv.fr/recherche/?what=&where=${where}&lat=${lat}&lon=${long}&code=${code}`;
  }

  $: accesslibreUrl = getAccessLibreUrl(structure);
</script>

<BasicInputField id="siret" bind:value={structure.siret} />

<BasicInputField
  id="name"
  bind:value={structure.name}
  placeholder="Plateforme de l’inclusion"
/>

<SelectField
  id="typology"
  bind:value={structure.typology}
  choices={structuresOptions.typologies}
  placeholder="Choisissez…"
  sort
/>

<FieldsAddress bind:entity={structure} />

<BasicInputField
  type="url"
  id="accesslibreUrl"
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
        rel="noopener ugc">acceslibre</a
      >
      et copiez l’url dans le champ ci-dessous.
    </small>
  </div>
</BasicInputField>

<BasicInputField
  type="tel"
  id="phone"
  bind:value={structure.phone}
  placeholder="0X XX XX XX XX"
/>

<BasicInputField
  type="email"
  id="email"
  bind:value={structure.email}
  placeholder="nom.prenom@organisation.fr"
/>

<BasicInputField
  type="url"
  id="url"
  bind:value={structure.url}
  placeholder="https://mastructure.fr"
/>

<TextareaField
  id="shortDesc"
  bind:value={structure.shortDesc}
  placeholder="Décrivez brièvement votre structure"
/>

<RichTextField
  id="fullDesc"
  bind:value={structure.fullDesc}
  placeholder="Présentation détaillée de la structure"
  vertical
/>

<MultiSelectField
  id="nationalLabels"
  bind:value={structure.nationalLabels}
  choices={structuresOptions.nationalLabels}
  description="Indiquez si la structure fait partie d’un ou plusieurs réseaux nationaux"
  placeholder="Choisissez…"
  placeholderMulti="Choisissez…"
  vertical
/>

<BasicInputField
  id="otherLabels"
  bind:value={structure.otherLabels}
  description="Indiquez si la structure fait partie d’autres labels (régionaux, locaux…)"
  vertical
/>

<OpeningHoursField
  id="openingHours"
  bind:value={structure.openingHours}
  vertical
/>

<BasicInputField
  id="openingHoursDetails"
  bind:value={structure.openingHoursDetails}
  description="Vous pouvez renseigner des informations spécifiques concernant les horaires dans ce champ"
  vertical
/>

<HiddenField id="ape" value={structure.ape} />
