<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/display/modal.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import type { Service } from "$lib/types";
  import { tick } from "svelte";

  export let service: Service;

  let isInclusionNumModalOpen = false;

  let inclusionNumeriqueFormActiveNotice = {
    title: "Formulaire de l'inclusion numérique actif",
    description:
      "Si néanmoins vous souhaitez renseigner un atelier, une formation ou tout autre accompagnement, vous pouvez basculer vers le formulaire classique.",
    buttonLabel: "Basculer sur le formulaire classique",
  };

  let inclusionNumeriqueFormAvailableNotice = {
    title: "Formulaire de l'inclusion numérique disponible",
    description:
      "Pour compléter ce formulaire spécifique, seule la thématique numérique doit être sélectionnée.",
    buttonLabel: "Basculer sur le formulaire inclusion numérique",
  };

  $: displayInclusionNumeriqueFormNotice =
    service.categories.includes("numerique");

  $: selectedInclusionNumeriqueFormNotice = service.useInclusionNumeriqueScheme
    ? inclusionNumeriqueFormActiveNotice
    : inclusionNumeriqueFormAvailableNotice;

  function toggleInclusionNumeriqueForm() {
    service.useInclusionNumeriqueScheme = !service.useInclusionNumeriqueScheme;

    if (service.useInclusionNumeriqueScheme) {
      service.categories = ["numerique"];
    } else {
      if (service.feeCondition === "pass-numerique") {
        service.feeCondition = "gratuit";
      }
    }
  }

  function openInclusionNumModal() {
    isInclusionNumModalOpen = true;
  }

  function handleRejectSwitchToInclusionNumForm() {
    isInclusionNumModalOpen = false;
  }

  async function handleSwitchToInclusionNumForm() {
    isInclusionNumModalOpen = false;
    toggleInclusionNumeriqueForm();
    await tick();
  }

  $: showModel = !!service.model;
</script>

<Modal
  bind:isOpen={isInclusionNumModalOpen}
  title="Attention !"
  smallWidth
  overflow
>
  Le passage du formulaire classique vers le formulaire de l'inclusion numérique
  peut entraîner la perte de données déjà enregistrées dans ce service.
  <div class="mt-s32 flex flex-row justify-end gap-s16">
    <Button
      label="Rester sur le formulaire classique"
      secondary
      on:click={handleRejectSwitchToInclusionNumForm}
    />
    <Button
      label="Passer au formulaire de l'inclusion numérique"
      on:click={handleSwitchToInclusionNumForm}
    />
  </div>
</Modal>

{#if displayInclusionNumeriqueFormNotice}
  <div class="mt-s16">
    <Notice title={selectedInclusionNumeriqueFormNotice.title} type="info">
      <p class="text-f14">
        Les services d'inclusion numérique répondent à un formulaire spécifique
        permettant une harmonie entre tous les acteurs du secteur.
        <br />
        {selectedInclusionNumeriqueFormNotice.description}
      </p>
      <p>
        <Button
          label={selectedInclusionNumeriqueFormNotice.buttonLabel}
          small
          noBackground
          noPadding
          on:click={service.useInclusionNumeriqueScheme
            ? toggleInclusionNumeriqueForm
            : openInclusionNumModal}
        />
      </p>
    </Notice>
  </div>
{/if}
