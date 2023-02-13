<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getStructureAdmin } from "$lib/requests/admin";
  import StructureContacts from "../structure-contacts.svelte";

  export let isOpen = false;
  export let structureSlug: string;

  let title: string;

  $: structurePromise = getStructureAdmin(structureSlug);
  $: structurePromise.then((struct) => {
    title = struct?.name || "";
  });
</script>

<Modal bind:isOpen {title} smallWidth overflow>
  {#await structurePromise}
    <p class="italic">Chargement…</p>
  {:then structure}
    <StructureContacts {structure} />
  {:catch error}
    <p style="color: red">{error.message}</p>
  {/await}
</Modal>
