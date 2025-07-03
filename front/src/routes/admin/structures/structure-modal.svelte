<script lang="ts">
  import { run } from 'svelte/legacy';

  import Modal from "$lib/components/hoc/modal.svelte";
  import { getStructureAdmin } from "$lib/requests/admin";
  import type { AdminShortStructure } from "$lib/types";
  import ModerationButtonMenu from "../moderation-button-menu.svelte";
  import StructureContacts from "../structure-contacts.svelte";

  interface Props {
    isOpen?: boolean;
    structureSlug: string | null;
    onRefresh: any;
  }

  let { isOpen = $bindable(false), structureSlug = $bindable(), onRefresh }: Props = $props();

  let structure: AdminShortStructure | null = $state(null);

  async function handleRefresh() {
    structure = structureSlug ? await getStructureAdmin(structureSlug) : null;
    if (onRefresh) {
      onRefresh();
    }
  }

  run(() => {
    (async () =>
      (structure = structureSlug
        ? await getStructureAdmin(structureSlug)
        : null))();
  });
</script>

<Modal
  on:close={() => (structureSlug = null)}
  bind:isOpen
  title={structure?.name}
  width="medium"
>
  <div class="m-s16">
    {#if structure}
      <ModerationButtonMenu entity={structure} onRefresh={handleRefresh} />
      <StructureContacts {structure} />
    {/if}
  </div>
</Modal>
