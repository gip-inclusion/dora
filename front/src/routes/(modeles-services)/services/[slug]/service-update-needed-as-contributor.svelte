<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/specialized/services/set-as-updated-modal.svelte";
  import UpdateNeededIcon from "$lib/components/specialized/services/update-needed-icon.svelte";
  import { checkboxCircleFillIcon, editIcon } from "$lib/icons";
  import type { Service, ServicesOptions } from "$lib/types";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  export let onRefresh: () => void;

  let setAsUpdatedModalOpen = false;
</script>

<div
  class="gap-s24 text-gray-text flex w-full flex-col place-content-between items-center sm:flex-row"
>
  <div id="label-container" class="flex-3">
    {#if service.status === "PUBLISHED"}
      {#if service.updateNeeded}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateNeededIcon updateNeeded={service.updateNeeded} />
          </span>
          <div>
            <div class="text-f18">
              <RelativeDateLabel
                date={service.modificationDate}
                prefix="Actualisé"
                bold
              />
            </div>
            <div class="text-f14">
              Vérifiez et/ou actualisez les informations de ce service dès
              maintenant pour qu’il reste visible.
            </div>
          </div>
        </div>
      {:else}
        <div class="flex items-center">
          <div class="mr-s16">
            <UpdateNeededIcon updateNeeded={service.updateNeeded} />
          </div>

          <RelativeDateLabel
            date={service.modificationDate}
            prefix="Actualisé"
          />
        </div>
      {/if}
    {/if}
  </div>
  <div class="md:mt-s0 flex w-full flex-2 flex-col justify-end lg:flex-row">
    {#if service.updateNeeded && service.status === "PUBLISHED"}
      <Button
        id="set-as-updated"
        extraClass="mb-s10 lg:mb-s0 lg:mr-s16 justify-center"
        label="Marquer comme à jour"
        icon={checkboxCircleFillIcon}
        on:click={() => (setAsUpdatedModalOpen = true)}
      />

      <SetAsUpdatedModal
        bind:isOpen={setAsUpdatedModalOpen}
        {service}
        {servicesOptions}
        {onRefresh}
      />
    {/if}

    <LinkButton
      id="update"
      label="Modifier"
      to="/services/{service.slug}/editer"
      icon={editIcon}
    />
  </div>
</div>
