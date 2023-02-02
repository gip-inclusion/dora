<script lang="ts">
  import Notice from "$lib/components/display/notice.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsPlace from "$lib/components/specialized/services/fields-place.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import type { Establishment, Service, ServicesOptions } from "$lib/types";

  export let servicesOptions: ServicesOptions;
  export let contribution: Service;
  export let establishment: Establishment;
</script>

{#if contribution.siret}
  <FieldsPresentation bind:service={contribution} {servicesOptions} />

  <FieldsTypology bind:service={contribution} {servicesOptions} />

  <div class="mt-s48">
    <Notice type="warning">
      <p class="text-f14">
        Renseignez le courriel du référent afin de faciliter la validation de
        votre suggestion.
      </p>
    </Notice>
  </div>

  <FieldsContact bind:service={contribution} />

  <div class="mt-s48">
    <Notice title="Informations facultatives">
      <p class="text-f14">
        Les informations ci-dessous sont facultatives, mais facilitent le
        travail des structures porteuses.
      </p>
    </Notice>
  </div>

  <FieldsPublics
    bind:service={contribution}
    {servicesOptions}
    canAddChoices={false}
  />

  <FieldsPlace
    bind:service={contribution}
    {servicesOptions}
    structure={establishment}
  />
{/if}
