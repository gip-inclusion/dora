<script>
  import { page } from "$app/stores";

  import { token } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import Label from "$lib/components/label.svelte";
  import {
    checkBoxBlankIcon,
    compassDiscoverIcon,
    mapPinIcon,
  } from "$lib/icons";

  export let service, structure;
  const editLink = `${$page.path}/edit`;
</script>

<style>
  .tags {
    display: flex;
    flex-direction: row;
    gap: var(--s16);
  }
</style>

<div class="col-start-1 col-span-full  mb-6  text-white">
  <div class="mx-auto">
    <Label label={structure.name} darkBg />
    <h1 class="text-white">{service.name}</h1>
    {#if $token}
      <div class="my-2">
        <LinkButton type="submit" to={editLink} label="Éditer" small />
      </div>
    {/if}
    <div class="tags">
      {#if service.isAvailable}
        <Label
          label="Disponible"
          iconOnLeft
          icon={checkBoxBlankIcon}
          success
          darkBg
          bold />
      {:else}
        <Label
          label="Indisponible"
          iconOnLeft
          icon={checkBoxBlankIcon}
          darkBg />
      {/if}
      {#each service.kindsDisplay as kind}
        <Label label={kind} iconOnLeft icon={compassDiscoverIcon} darkBg />
      {/each}

      <Label
        label={`${service.postalCode}, ${service.city}`}
        iconOnLeft
        icon={mapPinIcon}
        darkBg />
    </div>
  </div>
</div>
