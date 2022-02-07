<script>
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Tag from "$lib/components/tag.svelte";

  import { mapPinIcon } from "$lib/icons";

  export let structure, services;
</script>

<div class="col-span-full mt-s32">
  <div class="flex flex-col justify-between md:flex-row">
    <h2 class="text-france-blue">Derniers services ajoutés</h2>
    <LinkButton
      label="Voir tout"
      to="/structures/{structure.slug}/services"
      small
    />
  </div>
  <div class="md:grid-cols-s16 lg:grid-cols-s24 mt-s24 mb-s48 grid gap-s16">
    {#each services as service}
      <div class="rounded-md px-s20 py-s24 shadow-md">
        <h4><a href="/services/{service.slug}">{service.name}</a></h4>
        <div class="mt-s8 flex flex-col gap-s16">
          <Tag selfStart>{service.categoryDisplay}</Tag>
          <Label
            label={`${service.postalCode}, ${service.city}`}
            iconOnLeft
            smallIcon
            icon={mapPinIcon}
          />
        </div>
      </div>
    {/each}
  </div>
</div>
