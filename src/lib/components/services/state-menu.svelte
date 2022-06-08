<script>
  import { goto } from "$app/navigation";
  import {
    convertSuggestionToDraft,
    deleteService,
    getService,
    publishService,
    unPublishService,
  } from "$lib/services";

  import Button from "$lib/components/button.svelte";
  import { validate } from "$lib/validation";
  import schema, { fields, fieldsRequired } from "$lib/schemas/service.js";
  import { formatSchema } from "$lib/schemas/utils";

  export let service;
  export let onRefresh;
  export let secondary = false;

  const serviceSchema = formatSchema(
    schema,
    fields.service,
    fieldsRequired.service
  );

  async function handleUnpublish() {
    await unPublishService(service.slug);
    if (onRefresh) {
      await onRefresh();
    }
  }

  async function handlePublish() {
    let serviceFull = service;
    // teste si on a le service complet
    // ça n'est pas le cas sur la page structure par exemple
    if (!service.structure) {
      serviceFull = await getService(service.slug);
    }

    const isValid = validate(serviceFull, serviceSchema, {
      noScroll: true,
      showErrors: false,
    }).valid;

    if (isValid) {
      await publishService(service.slug);
      await onRefresh();
    } else {
      goto(`/services/${service.slug}/editer`);
    }
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
      label="Brouillon"
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
      label="Supprimer"
      on:click={() => {
        handleDelete(service);
      }}
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
{:else if !service.isDraft}
  <div>
    <Button
      label="Brouillon"
      on:click={() => {
        handleUnpublish(service);
      }}
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
{:else}
  <div>
    <Button
      label="Publié"
      on:click={() => {
        handlePublish(service);
      }}
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
{/if}
