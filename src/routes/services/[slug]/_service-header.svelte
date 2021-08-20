<script>
  import { page } from "$app/stores";

  import LinkButton from "$lib/components/link-button.svelte";

  export let service, structure;
  const editLink = `${$page.path}/edit`;
</script>

<div class="col-start-1 col-span-full  mb-6  text-white">
  <div class="mx-auto">
    <h3 class="text-white">
      {structure.name}
    </h3>
    <h1 class="text-white">{service.name}</h1>
    <LinkButton type="submit" to={editLink} label="Éditer" />
    {#if service.isAvailable}Disponible{:else}Indisponible{/if}
    {#each service.kindsDisplay as kind}
      {kind}
    {/each}
    {#each service.categoriesDisplay as cat}
      {cat}
    {/each}
    {service.postalCode}
    {service.city}
  </div>
</div>
