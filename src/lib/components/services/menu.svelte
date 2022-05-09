<script>
  import {
    convertSuggestionToDraft,
    deleteService,
    unPublishService,
  } from "$lib/services";

  import Button from "$lib/components/button.svelte";

  import LinkButton from "$lib/components/link-button.svelte";

  export let service;
  export let onRefresh;
  export let secondary = false;

  async function handleUnpublish() {
    await unPublishService(service.slug);
    await onRefresh();
  }

  async function handleConvertToDraft() {
    await convertSuggestionToDraft(service.slug);
    await onRefresh();
  }

  async function handleDelete() {
    // eslint-disable-next-line no-alert
    if (confirm(`Supprimer la suggestion ${service.name} ?`)) {
      await deleteService(service.slug);
      await onRefresh();
    }
  }
</script>

{#if service.isSuggestion}
  <div>
    <Button
      label="Convertir en brouillon"
      on:click={() => {
        handleConvertToDraft(service);
      }}
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
  <div>
    <Button
      label="Rejeter"
      on:click={() => {
        handleDelete(service);
      }}
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
{:else}
  {#if !service.isDraft}
    <div>
      <Button
        label="Désactiver"
        on:click={() => {
          handleUnpublish(service);
        }}
        small
        noBackground={!secondary}
        {secondary}
      />
    </div>
  {/if}
  <div>
    <LinkButton
      label="Modifier"
      to="/services/{service.slug}/editer"
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
{/if}
