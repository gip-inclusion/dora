<script lang="ts">
  import UpdateNeededIcon from "$lib/components/specialized/services/update-needed-icon.svelte";
  import type { Service } from "$lib/types";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";

  export let service: Service;
</script>

<div
  class="gap-s24 text-gray-text flex w-full flex-col place-content-between items-center md:flex-row"
>
  <div id="label-container">
    {#if service.status === "PUBLISHED"}
      <div class="flex items-center">
        <span class="mr-s16">
          <UpdateNeededIcon updateNeeded={service.updateNeeded} />
        </span>
        {#if service.updateNeeded}
          <div>
            <div class="text-f18">
              <RelativeDateLabel
                date={service.modificationDate}
                prefix="Actualisé"
                bold
              />
            </div>
            <div class="text-f14">
              Ce service n’a pas été actualisé récemment, certaines informations
              peuvent ne pas être à jour.
            </div>
          </div>
        {:else}
          <RelativeDateLabel
            date={service.modificationDate}
            prefix="Actualisé"
          />
        {/if}
      </div>
    {/if}
  </div>
</div>
