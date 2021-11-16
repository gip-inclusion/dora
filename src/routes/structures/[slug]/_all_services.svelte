<script>
  import Label from "$lib/components/label.svelte";
  import Tag from "$lib/components/tag.svelte";

  import { mapPinIcon } from "$lib/icons";

  export let services;
</script>

<div class="col-span-full mt-8 mb-6">
  <div class="flex flex-col gap-2">
    {#each services as service}
      <div class="shadow-md rounded-md px-5/2 py-3">
        <h4><a href="/services/{service.slug}">{service.name}</a></h4>
        <div class="flex flex-col gap-2">
          <div class="flex flex-row gap-2 mt-1 ">
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
          <div class="text-gray-text-alt2">{service.shortDesc}</div>
        </div>
      </div>
    {/each}
  </div>
</div>
