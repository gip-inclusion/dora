<script>
  import LinkButton from "$lib/components/link-button.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import Button from "../button.svelte";

  export let model;
  export let secondary = false;
  export let inline = false;

  async function createNewServiceLink() {
    await navigator.clipboard.writeText(
      `${CANONICAL_URL}/services/creer?modele=${model.slug}`
    );
  }
</script>

<div class:flex={inline} class:gap-s8={inline} class:items-start={inline}>
  <LinkButton
    label="Modifier"
    to="/modeles/{model.slug}/editer"
    small
    noBackground={!secondary}
    {secondary}
  />
  <div class="hidden">
    <Button
      label="Créer un service"
      on:click={createNewServiceLink}
      small
      noBackground={!secondary}
      {secondary}
    />
  </div>
</div>
