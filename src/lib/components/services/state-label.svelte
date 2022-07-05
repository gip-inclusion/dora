<script>
  import Label from "$lib/components/label.svelte";
  import { SERVICE_STATUSES } from "$lib/schemas/service";

  export let service;
</script>

{#if service.status === SERVICE_STATUSES.suggestion}
  <Label label="Suggestion" error bold />
{:else if service.status === SERVICE_STATUSES.draft}
  <Label label="Brouillon" wait bold />
{:else if service.status === SERVICE_STATUSES.published}
  <Label label="Publié" success bold />
{:else if service.status === SERVICE_STATUSES.archived}
  <Label label="Archivé" light bold />
{/if}
