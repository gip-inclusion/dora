<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import type { Service } from "$lib/types";

  interface Props {
    service: Service;
  }

  let { service = $bindable() }: Props = $props();

  let isSwitchModalOpen = $state(false);

  function activateInclusionNumForm() {
    service.useInclusionNumeriqueScheme = true;
    service.categories = ["numerique"];
  }

  function activateClassicForm() {
    service.useInclusionNumeriqueScheme = false;
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

  let currentNotice = $derived(
    service.useInclusionNumeriqueScheme
      ? inclusionNumFormActiveNotice
      : inclusionNumFormAvailableNotice
  );
</script>

<Modal bind:isOpen={isSwitchModalOpen} title="Attention !" width="small">
  Le passage du formulaire classique vers le formulaire de l’inclusion numérique
  peut entraîner la perte de données déjà enregistrées dans ce service.
  <div class="mt-s32 gap-s16 flex flex-row justify-end">
    <Button
      label="Rester sur le formulaire classique"
      secondary
      onclick={() => (isSwitchModalOpen = false)}
    />
    <Button
      label="Passer au formulaire de l’inclusion numérique"
      onclick={activateInclusionNumForm}
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
        onclick={currentNotice.action}
      />
    </p>
  </Notice>
</div>
