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
  import schema, {
    fields,
    fieldsRequired,
    SERVICE_STATUSES,
  } from "$lib/schemas/service.js";
  import { formatSchema } from "$lib/schemas/utils";

  export let service;
  export let onRefresh;
  export let secondary = false;

  const serviceSchema = formatSchema(
    schema,
    fields.service,
    fieldsRequired.service
  );

  async function unpublish() {
    await unPublishService(service.slug);
    if (onRefresh) {
      await onRefresh();
    }
  }

  async function publish() {
    let serviceFull = service;
    // teste si on a le service complet
    // ça n'est pas le cas sur les cards de la page structure par exemple

    if (!Object.prototype.hasOwnProperty.call(service, "fullDesc")) {
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

  async function convertToDraft() {
    await convertSuggestionToDraft(service.slug);
    await onRefresh();
  }

  async function remove() {
    // eslint-disable-next-line no-alert
    if (confirm(`Supprimer la suggestion ${service.name} ?`)) {
      await deleteService(service.slug);
      goto(`/structures/${service.structure}/`);
    }
  }
</script>

{#if service.status === SERVICE_STATUSES.suggestion}
  <Button
    label="Brouillon"
    on:click={convertToDraft}
    small
    noBackground={!secondary}
    {secondary}
  />

  <Button
    label="Supprimer"
    on:click={remove}
    small
    noBackground={!secondary}
    {secondary}
  />
{:else if service.status === SERVICE_STATUSES.published}
  <Button
    label="Brouillon"
    on:click={unpublish}
    small
    noBackground={!secondary}
    {secondary}
  />
{:else if service.status === SERVICE_STATUSES.draft}
  <Button
    label="Publié"
    on:click={publish}
    small
    noBackground={!secondary}
    {secondary}
  />
{/if}
