<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SetAsUpdatedModal from "$lib/components/specialized/services/set-as-updated-modal.svelte";
  import UpdateStatusIcon from "$lib/components/specialized/services/update-status-icon.svelte";
  import DateLabel from "$lib/components/utilities/date-label.svelte";
  import { checkboxCircleFillIcon, editIcon } from "$lib/icons";
  import type {
    Service,
    ServicesOptions,
    ServiceUpdateStatus,
  } from "$lib/types";

  export let service: Service;
  export let servicesOptions: ServicesOptions;

  export let label: string;
  export let updateStatus: ServiceUpdateStatus;
  export let onRefresh: () => void;

  let setAsUpdatedModalOpen = false;
</script>

<div
  class="flex w-full flex-col place-content-between items-center gap-s24 text-gray-text sm:flex-row"
>
  <div id="label-container" class="flex-[3]">
    {#if service.status === "PUBLISHED"}
      {#if updateStatus === "NOT_NEEDED"}
        <div class="flex items-center">
          <div class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </div>

          <span class="hidden print:inline">
            Mis à jour le <DateLabel date={service.modificationDate} />
          </span>
          <span class="print:hidden">{label}</span>
        </div>
      {:else if updateStatus === "NEEDED"}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </span>
          <div>
            <div class="text-f18">
              <strong class="hidden print:inline">
                Mis à jour le <DateLabel date={service.modificationDate} />
              </strong>
              <strong class="print:hidden">{label}</strong>
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
            <UpdateStatusIcon updateStatus="REQUIRED" />
          </span>
          <div>
            <div class="text-f18">
              <strong>Actualisation requise</strong>
            </div>
            <div class="text-f14">
              <strong class="hidden print:inline">
                Mis à jour le
                <DateLabel date={service.modificationDate} />
              </strong>
              <span class="print:hidden">
                Ce service est dépriorisé dans les résultats de recherche, il
                doit être actualisé pour gagner à nouveau en visibilité
              </span>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>
  <div class="flex w-full flex-[2] flex-col justify-end md:mt-s0 lg:flex-row">
    {#if updateStatus !== "NOT_NEEDED" && service.status === "PUBLISHED"}
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
