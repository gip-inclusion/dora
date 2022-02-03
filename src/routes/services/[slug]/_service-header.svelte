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

  export let service;
  export let isPreview = false;

  const editLink = `${$page.url.pathname}/editer`;
</script>

<div class="col-span-full col-start-1 mb-s48 text-white">
  <div class="mx-auto">
    <Label label={service.structureInfo.name} darkBg />
    <h1 class="text-white">{service.name}</h1>
    {#if $token && service.canWrite && !isPreview}
      <div class="noprint my-s16">
        <LinkButton to={editLink} label="Éditer" small />
      </div>
    {/if}
    <div class="flex flex-col gap-s16 md:flex-row">
      {#if service.isAvailable}
        <Label
          label="Disponible"
          iconOnLeft
          icon={checkBoxBlankIcon}
          success
          darkBg
          bold
        />
      {:else}
        <Label
          label="Indisponible"
          iconOnLeft
          icon={checkBoxBlankIcon}
          darkBg
        />
      {/if}

      <Label
        label={service.kindsDisplay.join(", ")}
        iconOnLeft
        icon={compassDiscoverIcon}
        darkBg
      />

      <Label
        label={`${service.postalCode}, ${service.city}`}
        iconOnLeft
        icon={mapPinIcon}
        darkBg
      />
    </div>
  </div>
</div>

<style lang="postcss">
  @media print {
    h1 {
      color: var(--col-france-blue);
    }
  }
</style>
