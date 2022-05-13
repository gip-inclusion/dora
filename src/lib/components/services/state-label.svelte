<script>
  import Label from "$lib/components/label.svelte";

  export let service;
</script>

{#if service.isSuggestion}
  <Label label="Suggestion" error bold />
{:else if service.isDraft}
  <Label label="Brouillon" wait bold />
{:else}
  <Label label="Publié" success bold />
{/if}
