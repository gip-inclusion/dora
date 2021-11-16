<script>
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Tag from "$lib/components/tag.svelte";

  import { mapPinIcon } from "$lib/icons";

  export let structure, services;
</script>

<div class="col-span-full mt-4">
  <div class="flex flex-col md:flex-row justify-between">
    <h2 class="text-france-blue">Derniers services ajoutés</h2>
    <LinkButton
      label="Voir tout"
      to="/structures/{structure.slug}/services"
      small
    />
  </div>
  <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-2 mt-3 mb-6">
    {#each services as service}
      <div class="shadow-md rounded-md px-5/2 py-3">
        <h4><a href="/services/{service.slug}">{service.name}</a></h4>
        <div class="flex flex-col gap-2 mt-1 ">
          <Tag
            --bg-color="var(--col-magenta-20)"
            --fg-color="var(--col-magenta-cta)">{service.categoryDisplay}</Tag
          >
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
