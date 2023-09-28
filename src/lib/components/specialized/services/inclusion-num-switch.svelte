<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import type { Service } from "$lib/types";

  export let service: Service;

  let isSwitchModalOpen = false;

  function activateInclusionNumForm() {
    service.useInclusionNumeriqueScheme = true;
    service.categories = ["numerique"];
  }

  function activateClassicForm() {
    service.useInclusionNumeriqueScheme = false;
    if (service.feeCondition === "pass-numerique") {
      service.feeCondition = "gratuit";
    }
  }

  const inclusionNumFormActiveNotice = {
    title: "Formulaire de l’inclusion numérique actif",
    description:
      "Si néanmoins vous souhaitez renseigner un atelier, une formation ou tout autre accompagnement, vous pouvez basculer vers le formulaire classique.",
    buttonLabel: "Basculer sur le formulaire classique",
    action: activateClassicForm,
  };

  const inclusionNumFormAvailableNotice = {
    title: "Formulaire de l’inclusion numérique disponible",
    description:
      "Pour compléter ce formulaire spécifique, seule la thématique numérique doit être sélectionnée.",
    buttonLabel: "Basculer sur le formulaire inclusion numérique",
    action: () => {
      isSwitchModalOpen = true;
    },
  };

  $: currentNotice = service.useInclusionNumeriqueScheme
    ? inclusionNumFormActiveNotice
    : inclusionNumFormAvailableNotice;
</script>

<Modal
  bind:isOpen={isSwitchModalOpen}
  title="Attention !"
  width="small"
  overflow
>
  Le passage du formulaire classique vers le formulaire de l’inclusion numérique
  peut entraîner la perte de données déjà enregistrées dans ce service.
  <div class="mt-s32 flex flex-row justify-end gap-s16">
    <Button
      label="Rester sur le formulaire classique"
      secondary
      on:click={() => (isSwitchModalOpen = false)}
    />
    <Button
      label="Passer au formulaire de l’inclusion numérique"
      on:click={activateInclusionNumForm}
    />
  </div>
</Modal>

<div class="mt-s16">
  <Notice title={currentNotice.title} type="info">
    <p class="text-f14">
      Les services d’inclusion numérique répondent à un formulaire spécifique
      permettant une harmonie entre tous les acteurs du secteur.
      <br />
      {currentNotice.description}
    </p>
    <p>
      <Button
        label={currentNotice.buttonLabel}
        small
        noBackground
        noPadding
        on:click={currentNotice.action}
      />
    </p>
  </Notice>
</div>
