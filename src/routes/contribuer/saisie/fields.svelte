<script lang="ts">
  import Notice from "$lib/components/display/notice.svelte";
  import StructureSearch from "$lib/components/specialized/establishment-search/search.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsPlace from "$lib/components/specialized/services/fields-place.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import { contribSchema } from "$lib/validation/schemas/service";

  export let servicesOptions: ServicesOptions;
  export let service: Service;

  let establishment = null;

  function handleStructureCityChange() {
    service.siret = "";
  }

  async function handleEstablishmentChange(newEstablishment) {
    service.siret = newEstablishment?.siret;
  }
</script>

<StructureSearch
  onEstablishmentChange={handleEstablishmentChange}
  onCityChange={handleStructureCityChange}
  bind:establishment
  isOwnStructure={false}
  schema={contribSchema}
/>

{#if service.siret}
  <FieldsPresentation bind:service {servicesOptions} schema={contribSchema} />

  <FieldsTypology bind:service {servicesOptions} schema={contribSchema} />

  <div class="mt-s48">
    <Notice type="warning">
      <p class="text-f14">
        Renseignez le courriel du référent afin de faciliter la validation de
        votre suggestion.
      </p>
    </Notice>
  </div>

  <FieldsContact bind:service required={false} schema={contribSchema} />

  <div class="mt-s48">
    <Notice title="Informations facultatives">
      <p class="text-f14">
        Les informations ci-dessous sont facultatives, mais facilitent le
        travail des structures porteuses.
      </p>
    </Notice>
  </div>

  <FieldsPublics
    bind:service
    schema={contribSchema}
    {servicesOptions}
    canAddChoices={false}
  />

  <FieldsPlace
    bind:service
    {servicesOptions}
    schema={contribSchema}
    structure={establishment}
  />
{/if}
