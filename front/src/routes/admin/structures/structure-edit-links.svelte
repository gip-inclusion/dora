<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import type { AdminStructure } from "$lib/types";

  import { hasAdminStatus } from "./structure-statuses";

  interface Props {
    structure: AdminStructure;
    small?: boolean;
  }

  let { structure, small = false }: Props = $props();

  const highlightAdmins = $derived(hasAdminStatus(structure));
</script>

<div class="gap-s16 flex flex-row flex-wrap justify-end">
  {#if !structure.isObsolete}
    <LinkButton
      label="Modifier les services"
      to="/structures/{structure.slug}/services"
      otherTab
      secondary
      {small}
    />
    <LinkButton
      label="Modifier la structure"
      to="/structures/{structure.slug}"
      otherTab
      secondary
      {small}
    />
  {/if}
  <LinkButton
    label="Gérer les administrateurs"
    to="/structures/{structure.slug}/collaborateurs"
    otherTab
    secondary={!highlightAdmins}
    {small}
  />
</div>
