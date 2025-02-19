<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import DenyOrientationModal from "./deny-orientation-modal.svelte";
  import AcceptOrientationModal from "./accept-orientation-modal.svelte";
  import ContactBeneficiaryModal from "./contact-beneficiary-modal.svelte";
  import ContactPrescriberModal from "./contact-prescriber-modal.svelte";
  import { browser } from "$app/environment";
  import type { Orientation } from "$lib/types";
  import Notice from "$lib/components/display/notice.svelte";
  import { formatNumericDate } from "$lib/utils/date";

  export let orientation: Orientation;
  export let queryHash: string;
  export let onRefresh;

  let modalOpened:
    | "accept"
    | "deny"
    | "contact-beneficiary"
    | "contact-service"
    | undefined = undefined;

  function closeModal() {
    modalOpened = undefined;
  }

  let statusMessage: { label?: string; cssClass?: string } = {};
  $: {
    if (orientation.status === "VALIDÉE") {
      statusMessage = { label: "Validé", cssClass: "text-success" };
    } else if (orientation.status === "OUVERTE") {
      statusMessage = {
        label: "Ouverte / En cours de traitement",
        cssClass: "text-blue-information-dark",
      };
    } else if (orientation.status === "REFUSÉE") {
      statusMessage = { label: "Refusé", cssClass: "text-error" };
    }
  }
</script>

{#if browser}
  <DenyOrientationModal
    isOpen={modalOpened === "deny"}
    on:close={closeModal}
    {orientation}
    {queryHash}
    {onRefresh}
  />
  <AcceptOrientationModal
    isOpen={modalOpened === "accept"}
    on:close={closeModal}
    {orientation}
    {queryHash}
    {onRefresh}
  />
  <ContactBeneficiaryModal
    isOpen={modalOpened === "contact-beneficiary"}
    on:close={closeModal}
    {onRefresh}
    {orientation}
    {queryHash}
  />
  <ContactPrescriberModal
    isOpen={modalOpened === "contact-service"}
    on:close={closeModal}
    {orientation}
    {queryHash}
    {onRefresh}
  />
{/if}

<div class="border-gray-02 p-s32 rounded-lg border">
  <h2>Traiter la demande</h2>

  {#if !orientation.service?.slug}
    <Notice type="error" title="Traitement impossible">
      Le service « {orientation.service?.name} » n’existe plus.
    </Notice>
  {:else}
    <div class="mb-s24">
      <strong class="text-gray-text">Statut de la demande:<br /></strong>
      {#if statusMessage.label}
        <span class={statusMessage.cssClass}>
          {statusMessage.label}
        </span>
      {/if}
    </div>

    {#if orientation.status === "OUVERTE"}
      <div class="gap-s12 flex flex-col">
        <Button
          label="Valider la demande"
          on:click={() => (modalOpened = "accept")}
        />
        <Button
          secondary
          label="Refuser la demande"
          extraClass="border-error! text-error! hover:text-white! hover:border-error hover:bg-error!"
          on:click={() => (modalOpened = "deny")}
        />

        {#if orientation.beneficiaryEmail}
          <Button
            secondary
            extraClass="border-gray-dark! text-gray-text! hover:text-white! hover:border-gray-dark hover:bg-gray-dark!"
            label="Contacter le ou la bénéficiaire"
            on:click={() => (modalOpened = "contact-beneficiary")}
          />
        {/if}

        <Button
          secondary
          extraClass="border-gray-dark! text-gray-text! hover:text-white! hover:border-gray-dark hover:bg-gray-dark!"
          label="Contacter le ou la prescripteur·rice"
          on:click={() => (modalOpened = "contact-service")}
        />
      </div>
    {:else if orientation.status === "VALIDÉE"}
      <Notice
        type="info"
        title="Vous avez validé cette demande le {formatNumericDate(
          orientation.processingDate
        )}"
      >
        <p class="text-f14 text-gray-text text-left">
          Vous ne pouvez plus revenir sur une décision qui a déjà été actée.
        </p>
      </Notice>
    {:else if orientation.status === "REFUSÉE"}
      <Notice
        type="error"
        title="Vous avez refusé cette demande le {formatNumericDate(
          orientation.processingDate
        )}"
      >
        <p class="text-f14 text-gray-text text-left">
          Vous ne pouvez plus revenir sur une décision qui a déjà été actée.
        </p>
      </Notice>
    {/if}
  {/if}
</div>
