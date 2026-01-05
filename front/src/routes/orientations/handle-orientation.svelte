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

  const statusMap = {
    VALIDÉE: { label: "Validée", cssClass: "text-success" },
    OUVERTE: {
      label: "Ouverte / En cours de traitement",
      cssClass: "text-blue-information-dark",
    },
    REFUSÉE: { label: "Refusée", cssClass: "text-error" },
    EXPIRÉE: { label: "Expirée", cssClass: "text-warning" },
  };
  interface Props {
    orientation: Orientation;
    queryHash: string;
    onRefresh: any;
  }

  let { orientation, queryHash, onRefresh }: Props = $props();

  let modalOpened:
    | "accept"
    | "deny"
    | "contact-beneficiary"
    | "contact-service"
    | undefined = $state(undefined);

  function closeModal() {
    modalOpened = undefined;
  }

  const statusMessage = $derived(statusMap[orientation.status] || {});
</script>

{#if browser}
  <DenyOrientationModal
    isOpen={modalOpened === "deny"}
    onClose={closeModal}
    {orientation}
    {queryHash}
    {onRefresh}
  />
  <AcceptOrientationModal
    isOpen={modalOpened === "accept"}
    onClose={closeModal}
    {orientation}
    {queryHash}
    {onRefresh}
  />
  <ContactBeneficiaryModal
    isOpen={modalOpened === "contact-beneficiary"}
    onClose={closeModal}
    {onRefresh}
    {orientation}
    {queryHash}
  />
  <ContactPrescriberModal
    isOpen={modalOpened === "contact-service"}
    onClose={closeModal}
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
          onclick={() => (modalOpened = "accept")}
        />
        <Button
          secondary
          label="Refuser la demande"
          extraClass="border-error! text-error! hover:text-white! hover:border-error hover:bg-error!"
          onclick={() => (modalOpened = "deny")}
        />

        {#if orientation.beneficiaryEmail}
          <Button
            secondary
            extraClass="border-gray-dark! text-gray-text! hover:text-white! hover:border-gray-dark hover:bg-gray-dark!"
            label="Contacter le ou la bénéficiaire"
            onclick={() => (modalOpened = "contact-beneficiary")}
          />
        {/if}

        <Button
          secondary
          extraClass="border-gray-dark! text-gray-text! hover:text-white! hover:border-gray-dark hover:bg-gray-dark!"
          label="Contacter le ou la prescripteur·rice"
          onclick={() => (modalOpened = "contact-service")}
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
    {:else if orientation.status === "EXPIRÉE"}
      <Notice
        type="warning"
        title="N’ayant pas reçu de réponse, cette demande a expiré."
      >
        <p class="text-f14 text-gray-text text-left">
          Une demande d'orientation reçue requiert une réponse du service dans
          un délai maximal de 30 jours. Passé ce délai, cette demande est
          automatiquement annulée. Le prescripteur a été tenu informé de cette
          expiration.
        </p>
      </Notice>
    {/if}
  {/if}
</div>
