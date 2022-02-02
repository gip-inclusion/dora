<script>
  import {
    deleteServiceSuggestion,
    acceptServiceSuggestion,
  } from "$lib/services";

  import Button from "$lib/components/button.svelte";
  import ServiceSuggestionModal from "./_service-suggestion-modal.svelte";

  import { arrowRightSIcon, closeCircleIcon } from "$lib/icons";

  export let suggestions;
  export let onRefresh;

  let currentSuggestion;
  let modalIsOpen = false;

  async function handleAccept(suggestion) {
    if (confirm(`Accepter la suggestion ${suggestion.name} ?`)) {
      await acceptServiceSuggestion(suggestion);
      await onRefresh();
      modalIsOpen = false;
    }
  }

  async function handleReject(suggestion) {
    if (confirm(`Supprimer la suggestion ${suggestion.name} ?`)) {
      await deleteServiceSuggestion(suggestion);
      await onRefresh();
      modalIsOpen = false;
    }
  }
</script>

<ServiceSuggestionModal
  bind:isOpen={modalIsOpen}
  suggestion={currentSuggestion}
  onAccept={(s) => handleAccept(s)}
  onReject={(s) => handleReject(s)}
/>

<div class="flex flex-col gap-s12 w-full">
  {#each suggestions as suggestion}
    <div class="flex flex-row gap-s16 p-s16 bg-white rounded-md items-center">
      <div class="italic flex-1 truncate">
        {suggestion.name}
      </div>
      <div class="font-bold flex-1 text-ellipsis">
        {suggestion.structureInfo.name} ({suggestion.structureInfo.department})
        {#if suggestion.structureInfo.new}
          <div
            class="inline-block text-white text-f12 uppercase leading-20 bg-magenta-brand rounded px-s8 py-s2"
          >
            NOUV.
          </div>
        {/if}
      </div>

      <div class="flex flex-col flex-1 text-gray-text-alt truncate">
        {#if suggestion.creator}
          <div class="truncate">{suggestion.creator.getFullName}</div>
          <div class="truncate">{suggestion.creator.email}</div>
        {:else}<div class="truncate">ANONYME</div>
        {/if}
      </div>
      <div class="flex-none">
        <Button
          label="Rejeter"
          iconOnRight
          icon={closeCircleIcon}
          noBackground
          on:click={() => {
            handleReject(suggestion);
          }}
        />
      </div>
      <div class="flex-none">
        <Button
          label="Détails"
          iconOnRight
          icon={arrowRightSIcon}
          noBackground
          on:click={() => {
            currentSuggestion = suggestion;
            modalIsOpen = true;
          }}
        />
      </div>
    </div>
  {/each}
</div>
