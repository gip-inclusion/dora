<script lang="ts">
  import type { Service } from "$lib/types";
  import { SERVICE_UPDATE_STATUS, SERVICE_STATUSES } from "$lib/types";
  import LinkButton from "$lib/components/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/services/set-as-updated-modal.svelte";

  import UpdateStatusIcon from "$lib/components/services/icons/update-status.svelte";

  import { checkboxCircleFillIcon, editIcon } from "$lib/icons";
  import Button from "$lib/components/button.svelte";

  export let service: Service;

  export let label: string;
  export let monthDiff: number;
  export let updateStatus: SERVICE_UPDATE_STATUS;
  export let onRefresh: () => void;

  let setAsUpdatedModalOpen = false;
</script>

<div
  class="flex w-full flex-col place-content-between items-center gap-s24 text-gray-text sm:flex-row"
>
  <div id="label-container" class="flex-[3]">
    {#if service.status === SERVICE_STATUSES.PUBLISHED}
      {#if updateStatus === SERVICE_UPDATE_STATUS.NOT_NEEDED}
        <div class="flex items-center">
          <div class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </div>
          <span>{label}</span>
        </div>
      {:else if updateStatus === SERVICE_UPDATE_STATUS.NEEDED}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </span>
          <div>
            <div class="text-f18">
              <strong>{label}</strong>
            </div>
            <div class="text-f14">
              Vérifiez et/ou actualisez les informations de ce service dès
              maintenant pour qu’il reste visible.
            </div>
          </div>
        </div>
      {:else}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon updateStatus={SERVICE_UPDATE_STATUS.REQUIRED} />
          </span>
          <div>
            <div class="text-f18">
              <strong>Actualisation requise</strong>
            </div>
            <div class="text-f14">
              Ce service est dépriorisé dans les résultats de recherche, il doit
              être actualisé pour gagner à nouveau en visibilité
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>
  <div class="flex w-full flex-[2] flex-col justify-end md:mt-s0 lg:flex-row">
    {#if updateStatus !== SERVICE_UPDATE_STATUS.NOT_NEEDED && service.status === SERVICE_STATUSES.PUBLISHED}
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
