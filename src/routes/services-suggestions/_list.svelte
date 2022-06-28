<script>
  import {
    deleteServiceSuggestion,
    acceptServiceSuggestion,
  } from "$lib/services";

  import Button from "$lib/components/button.svelte";
  import Modal from "./_modal.svelte";

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

<Modal
  bind:isOpen={modalIsOpen}
  suggestion={currentSuggestion}
  onAccept={(s) => handleAccept(s)}
  onReject={(s) => handleReject(s)}
/>

<div class="flex w-full flex-col gap-s12">
  {#each suggestions as suggestion}
    <div class="flex flex-row items-center gap-s16 rounded-md bg-white p-s16">
      <div class="flex-1 truncate italic">
        {suggestion.name}
      </div>
      <div class="flex-1 text-ellipsis font-bold">
        {suggestion.structureInfo.name} ({suggestion.structureInfo.department})
        {#if suggestion.structureInfo.new}
          <div
            class="inline-block rounded bg-info px-s8 py-s2 text-f12 leading-20 text-white"
          >
            Nouv.
          </div>
        {/if}
      </div>

      <div class="flex flex-1 flex-col truncate text-gray-text-alt">
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
