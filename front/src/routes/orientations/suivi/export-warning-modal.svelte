<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import Button from "$lib/components/display/button.svelte";
  import CloseLineSystem from "svelte-remix/CloseLineSystem.svelte";
  import { orientationState } from "./state.svelte";

  interface Props {
    isOpen: boolean;
    handleClose: () => void;
    handleSubmit: () => void;
  }

  const { isOpen, handleClose, handleSubmit }: Props = $props();
</script>

<Modal {isOpen} width="small" hideCloseButton hideTitle>
  <div class="gap-s16 flex flex-col">
    <div class="flex justify-between">
      <h3 class="w-2xl">
        Téléchargement soumis à la protection des données personnelles (RGPD)
      </h3>
      <div>
        <Button
          icon={CloseLineSystem}
          onclick={handleClose}
          label="Fermer"
          noBackground
          noPadding
        />
      </div>
    </div>
    <p>
      Vous êtes sur le point de télécharger le <b
        >fichier des orientations {orientationState.selectedType === "sent"
          ? "envoyées"
          : "reçues"}</b
      >. Celui-ci contient des données personnelles permettant d’identifier les
      usagers.
    </p>
    <p>
      À ce titre, vous êtes tenu de respecter les exigences du <b
        >Règlement Général sur la Protection des Données (RGPD)</b
      > pour toute donnée exportée.
    </p>
    <p>
      Pour plus d’informations, vous pouvez consulter notre page de <a
        href="/politique-de-confidentialite"
        target="_blank"
        rel="noopener noreferrer"
        class="text-magenta-cta">protection des données personnelles.</a
      >
    </p>
    <div class="gap-s8 flex flex-col md:flex-row md:justify-end">
      <Button secondary label="Annuler" onclick={handleClose} />
      <Button
        label="Confirmer et télécharger le fichier"
        onclick={handleSubmit}
        id={`download-export-${orientationState.selectedType}`}
      />
    </div>
  </div></Modal
>
