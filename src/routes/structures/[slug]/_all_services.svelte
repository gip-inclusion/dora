<script>
  import Label from "$lib/components/label.svelte";
  import Tag from "$lib/components/tag.svelte";

  import { mapPinIcon } from "$lib/icons";

  export let services;
</script>

<div class="col-span-full mt-s64 mb-s48">
  <div class="flex flex-col gap-s16">
    {#each services as service}
      <div class="shadow-md rounded-md px-s20 py-s24">
        <h4><a href="/services/{service.slug}">{service.name}</a></h4>
        <div class="flex flex-col gap-s16">
          <div class="flex flex-row gap-s16 mt-s8">
            <Tag>{service.categoryDisplay}</Tag>
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
