<script>
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Tag from "$lib/components/tag.svelte";

  import { mapPinIcon } from "$lib/icons";

  export let structure, services;
</script>

<div class="col-span-full mt-s32">
  <div class="flex flex-col md:flex-row justify-between">
    <h2 class="text-france-blue">Derniers services ajoutés</h2>
    <LinkButton
      label="Voir tout"
      to="/structures/{structure.slug}/services"
      small
    />
  </div>
  <div class="grid md:grid-cols-2 lg:grid-cols-s24 gap-s16 mt-s24 mb-s48">
    {#each services as service}
      <div class="shadow-md rounded-md px-s20 py-s24">
        <h4><a href="/services/{service.slug}">{service.name}</a></h4>
        <div class="flex flex-col gap-s16 mt-s8">
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
