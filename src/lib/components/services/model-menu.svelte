<script>
  import { CANONICAL_URL } from "$lib/env";
  import { token, userInfo } from "$lib/auth";
  import { getStructures } from "$lib/structures";

  import LinkButton from "$lib/components/link-button.svelte";
  import Button from "$lib/components/button.svelte";
  import ModelStructureModal from "./model-structure-modal.svelte";

  export let model;
  export let secondary = false;
  export let inline = false;

  async function copyLink() {
    await navigator.clipboard.writeText(
      `${CANONICAL_URL}/modeles/${model.slug}`
    );
  }

  let structureModalOpened = false;
  let structures;
  async function openStructureModal() {
    structures = await getStructures();
    structureModalOpened = true;
  }
</script>

<ModelStructureModal
  isOpen={structureModalOpened}
  {structures}
  modelSlug={model.slug}
/>

<div class:flex={inline} class:gap-s8={inline} class:items-start={inline}>
  {#if $token && model.canWrite}
    <LinkButton
      label="Modifier"
      to="/modeles/{model.slug}/editer"
      small
      noBackground={!secondary}
      {secondary}
    />
  {/if}
  {#if $userInfo}
    <Button
      label="Créer un service"
      small
      on:click={openStructureModal}
      noBackground={!secondary}
      {secondary}
    />
  {/if}
  {#if false}
    <Button
      label="Copier le lien"
      on:click={copyLink}
      small
      noBackground={!secondary}
      {secondary}
    />
  {/if}
</div>
