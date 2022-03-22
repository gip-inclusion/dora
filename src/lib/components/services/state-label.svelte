<script>
  import Label from "$lib/components/label.svelte";
  import { checkBoxBlankIcon } from "$lib/icons";
  export let service;
</script>

{#if service.isSuggestion}
  <Label label="Suggestion" icon={checkBoxBlankIcon} smallIcon error bold />
{:else if service.isDraft}
  <Label label="Brouillon" icon={checkBoxBlankIcon} smallIcon wait bold />
{:else}
  <Label label="Publié" icon={checkBoxBlankIcon} smallIcon success bold />
{/if}
