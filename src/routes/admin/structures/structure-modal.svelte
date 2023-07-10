<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getStructureAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure } from "$lib/types";
  import ModerationButtonMenu from "../moderation-button-menu.svelte";
  import StructureContacts from "../structure-contacts.svelte";

  export let isOpen = false;
  export let structureSlug: string | null;
  export let onRefresh;

  let structure: AdminShortStructure | null = null;

  async function handleRefresh() {
    structure = structureSlug ? await getStructureAdmin(structureSlug) : null;
    if (onRefresh) {
      onRefresh();
    }
  }

  $: (async () =>
    (structure = structureSlug
      ? await getStructureAdmin(structureSlug)
      : null))();
</script>

<Modal
  on:close={() => (structureSlug = null)}
  bind:isOpen
  title={structure?.name}
  width="small"
  overflow
>
  {#if structure}
    <ModerationButtonMenu entity={structure} onRefresh={handleRefresh} />
    <StructureContacts {structure} />
  {/if}
</Modal>
