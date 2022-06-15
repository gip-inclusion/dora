<script>
  import LinkButton from "$lib/components/link-button.svelte";

  export let service;
  export let inline = false;
</script>

<div class:flex={inline} class:gap-s8={inline} class:items-start={inline}>
  {#if service.model}
    <LinkButton
      label="Modifier"
      to="/services/{service.slug}/editer"
      small
      noBackground
    />
    <div class="py-s6 text-gray-02" class:hidden={!inline}>|</div>

    <LinkButton
      label="Voir le modèle"
      to="/modeles/{service.model}"
      small
      noBackground
    />
  {:else}
    <LinkButton
      label="Modifier"
      to="/services/{service.slug}/editer"
      small
      noBackground={!inline}
      secondary={inline}
    />
    <LinkButton
      label="Créer un modèle"
      to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
      small
      secondary={inline}
      noBackground={!inline}
    />
  {/if}
</div>
