<script>
  import LinkButton from "$lib/components/link-button.svelte";

  export let service;
  export let secondary = false;
  export let inline = false;
</script>

<div class:flex={inline} class:gap-s8={inline} class:items-start={inline}>
  <LinkButton
    label="Modifier"
    to="/services/{service.slug}/editer"
    small
    noBackground={!secondary}
    {secondary}
  />

  {#if service.model}
    <LinkButton
      label="Voir le modèle"
      to="/modeles/{service.model}"
      small
      noBackground={!secondary}
      {secondary}
    />
  {:else}
    <LinkButton
      label="Créer un modèle"
      to={`/modeles/creer?service=${service.slug}`}
      small
      {secondary}
      noBackground={!secondary}
    />
  {/if}
</div>
