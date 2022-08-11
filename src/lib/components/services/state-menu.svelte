<script>
  import { goto } from "$app/navigation";
  import {
    convertSuggestionToDraft,
    deleteService,
    getService,
    publishService,
    unPublishService,
    archiveService,
    unarchiveService,
  } from "$lib/services";

  import Button from "$lib/components/button.svelte";
  import { validate } from "$lib/validation";
  import { serviceSchema, SERVICE_STATUSES } from "$lib/schemas/service.js";

  export let service, servicesOptions;
  export let onRefresh;
  export let secondary = false;

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
      extraData: servicesOptions,
    }).valid;

    if (isValid) {
      await publishService(service.slug);
      await onRefresh();
    } else {
      goto(`/services/${service.slug}/editer`);
    }
  }

  async function archive() {
    await archiveService(service.slug);
    if (onRefresh) {
      await onRefresh();
    }
  }

  async function unarchive() {
    await unarchiveService(service.slug);
    if (onRefresh) {
      await onRefresh();
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
  <Button
    label="Archivé"
    on:click={archive}
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
  <Button
    label="Archivé"
    on:click={archive}
    small
    noBackground={!secondary}
    {secondary}
  />
{:else if service.status === SERVICE_STATUSES.archived}
  <Button
    label="Brouillon"
    on:click={unarchive}
    small
    noBackground={!secondary}
    {secondary}
  />
{/if}
