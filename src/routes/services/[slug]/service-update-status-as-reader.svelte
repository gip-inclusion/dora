<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import UpdateStatusIcon from "$lib/components/specialized/services/update-status-icon.svelte";
  import DateLabel from "$lib/components/utilities/date-label.svelte";
  import { editIcon } from "$lib/icons";
  import type { Service, ServiceUpdateStatus } from "$lib/types";
  import { trackSuggestion } from "$lib/utils/plausible";
  import SuggestionModal from "./suggestion-modal.svelte";

  export let service: Service;

  export let label: string;
  export let monthDiff: number;
  export let updateStatus: ServiceUpdateStatus;

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
    {#if service.status === "PUBLISHED"}
      {#if updateStatus === "NOT_NEEDED"}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon {updateStatus} />
          </span>

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
                Mis à jour le
                <DateLabel date={service.modificationDate} />
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
            <UpdateStatusIcon updateStatus="REQUIRED" />
          </span>
          <div>
            <div class="text-f18">
              <strong>Service en attente d’actualisation</strong>
            </div>
            <div class="text-f14">
              <strong class="hidden print:inline">
                Mis à jour le
                <DateLabel date={service.modificationDate} />
              </strong>
              <span class="print:hidden">
                Les informations sur ce service n’ont plus été mises à jour
                depuis {monthDiff}
                mois.
              </span>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>

  <div class="print:hidden">
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
