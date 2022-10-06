<script lang="ts">
  import { trackSuggestion } from "$lib/utils/plausible";

  import {
    type Service,
    SERVICE_UPDATE_STATUS,
    SERVICE_STATUSES,
  } from "$lib/types";
  import Button from "$lib/components/button.svelte";
  import SuggestionModal from "$lib/components/services/suggestion-modal.svelte";

  import UpdateStatusIcon from "$lib/components/services/icons/update-status.svelte";

  import { editIcon } from "$lib/icons";
  import Date from "$lib/components/date.svelte";

  export let service: Service;

  export let label: string;
  export let monthDiff: number;
  export let updateStatus: SERVICE_UPDATE_STATUS;

  // Suggestion modal
  let suggestionModalIsOpen = false;

  function handleSuggestion() {
    suggestionModalIsOpen = true;
    trackSuggestion(service);
  }
</script>

<div
  class="flex w-full flex-col place-content-between items-center gap-s24 text-gray-text md:flex-row"
>
  <div id="label-container">
    {#if service.status === SERVICE_STATUSES.PUBLISHED}
      {#if updateStatus === SERVICE_UPDATE_STATUS.NOT_NEEDED}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </span>

          <span class="hidden print:inline">
            Mis à jour le <Date date={service.modificationDate} />
          </span>
          <span class="print:hidden">{label}</span>
        </div>
      {:else if updateStatus === SERVICE_UPDATE_STATUS.NEEDED}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </span>
          <div>
            <div class="text-f18">
              <strong class="hidden print:inline">
                Mis à jour le <Date date={service.modificationDate} />
              </strong>
              <strong class="print:hidden">{label}</strong>
            </div>
            <div class="text-f14">
              Ce service n’a pas été actualisé récemment, certaines informations
              peuvent ne pas être à jour.
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
              <strong>Service en attente d’actualisation</strong>
            </div>
            <div class="text-f14">
              Les informations sur ce service n’ont plus été mises à jour depuis {monthDiff}
              mois.
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>

  <div class="noprint">
    <SuggestionModal {service} bind:isOpen={suggestionModalIsOpen} />
    <Button
      id="suggest-update"
      label="Suggérer une modification"
      icon={editIcon}
      secondary
      small
      extraClass="py-s9"
      on:click={handleSuggestion}
    />
  </div>
</div>
