<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/display/modal.svelte";
  import { arrowRightSIcon, closeCircleIcon } from "$lib/icons";
  import {
    acceptServiceSuggestion,
    deleteServiceSuggestion,
  } from "$lib/requests/services";
  import SuggestionModal from "./suggestion-modal.svelte";

  export let suggestions;
  export let onRefresh;

  let currentSuggestion;
  let suggestionModalIsOpen = false;
  let confirmationModalIsOpen = false;
  let emailsContacted = null;

  async function handleAccept(suggestion) {
    // eslint-disable-next-line no-alert
    if (confirm(`Accepter la suggestion ${suggestion.name} ?`)) {
      const result = await acceptServiceSuggestion(suggestion);

      // On confirme que la suggestion a bien été transformé en service
      if (!result.ok) {
        // eslint-disable-next-line no-alert
        alert(result.error.detail.message); // FIXME: message "Pas trouvé." peu pertinent
      } else {
        emailsContacted = result?.data?.emailsContacted ?? [];
        suggestionModalIsOpen = false;
        confirmationModalIsOpen = true;
      }
    }
  }

  async function onConfirmationClose() {
    confirmationModalIsOpen = false;
    emailsContacted = null;
    await onRefresh();
  }

  async function handleReject(suggestion) {
    // eslint-disable-next-line no-alert
    if (confirm(`Supprimer la suggestion ${suggestion.name} ?`)) {
      await deleteServiceSuggestion(suggestion);
      await onRefresh();
      suggestionModalIsOpen = false;
    }
  }
</script>

<SuggestionModal
  bind:isOpen={suggestionModalIsOpen}
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
            suggestionModalIsOpen = true;
          }}
        />
      </div>
    </div>
  {/each}
</div>

<Modal
  bind:isOpen={confirmationModalIsOpen}
  on:close={onConfirmationClose}
  title="Création du service réussie"
  overflow
>
  {#if emailsContacted}
    {#if emailsContacted.length === 0}
      <p>
        Toutefois, aucun courriel n’a été envoyé car aucun destinataire n’a pu
        être déterminé…
      </p>
    {:else}
      <p>
        La ou les personnes suivantes ont reçu un courriel les invitant à
        prendre connaissance de ce nouveau service&nbsp;:
      </p>
      <ul class="list-disc pl-s32">
        {#each emailsContacted as mail}
          <li>{mail}</li>
        {/each}
      </ul>
    {/if}
  {/if}
</Modal>
