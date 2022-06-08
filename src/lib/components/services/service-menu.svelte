<script>
  import { goto } from "$app/navigation";

  import LinkButton from "$lib/components/link-button.svelte";
  import { createModelFromService } from "$lib/services";
  import Button from "../button.svelte";

  export let service;
  export let secondary = false;
  export let inline = false;

  async function createModel() {
    const result = await createModelFromService(
      service.slug,
      service.structure
    );

    goto(`/modeles/${result.data.slug}`);
  }
</script>

<div class:flex={inline} class:gap-s8={inline} class:items-start={inline}>
  <LinkButton
    label="Modifier"
    to="/services/{service.slug}/editer"
    small
    noBackground={!secondary}
    {secondary}
  />
  <!-- ajouter une condition pour n'afficher le bouton que si le service n'est pas lié à un modèle -->
  {#if service.model}
    <LinkButton
      label="Voir le modèle"
      to="/modeles/{service.model}"
      small
      noBackground={!secondary}
      {secondary}
    />
  {:else}
    <Button
      label="Créer un modèle"
      small
      {secondary}
      on:click={createModel}
      noBackground={!secondary}
    />
  {/if}
</div>
