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
    <div
      class="flex items-center rounded"
      class:border={secondary}
      class:border-gray-01={secondary}
    >
      <div class="px-s12 py-s6 text-f14 font-bold text-gray-text">
        Synchronisé
      </div>
      <div class="text-gray-02">|</div>

      <LinkButton
        label="Voir le modèle"
        to="/modeles/{service.model}"
        small
        noBackground
      />
    </div>
  {:else}
    <LinkButton
      label="Créer un modèle"
      to={`/modeles/creer?service=${service.slug}&structure=${service.structure}`}
      small
      {secondary}
      noBackground={!secondary}
    />
  {/if}
</div>
