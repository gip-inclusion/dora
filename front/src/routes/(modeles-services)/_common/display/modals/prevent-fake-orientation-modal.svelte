<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { browser } from "$app/environment";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  export let isOpen = false;
  export let orientationFormUrl: string;

  const dispatch = createEventDispatcher<{
    showVideo: object;
    trackMobilisation: object;
  }>();
</script>

{#if browser}
  <Modal bind:isOpen title="Avant de continuer" width="medium">
    <p>
      ⚠️ <strong>Rappel :</strong> Les orientations fictives, destinées à tester
      l’outil, nécessitent une vérification manuelle, ajoutant une charge de travail
      pour nos équipes.
    </p>
    <p>
      Nous vous invitons à consulter notre <a
        href="https://aide.dora.inclusion.beta.gouv.fr/fr/category/orienter-vos-beneficiaires-c25cna/"
        target="_blank"
        class="text-magenta-cta underline">documentation</a
      > ou voir la vidéo de présentation pour comprendre l’utilisation du formulaire
      d’orientation.
    </p>
    <div slot="footer" class="flex justify-end gap-s12">
      <LinkButton
        label="Poursuivre l’orientation"
        secondary
        to={orientationFormUrl}
        on:click={() => dispatch("trackMobilisation", {})}
      />
      <Button
        label="Regarder la vidéo"
        on:click={() => dispatch("showVideo", {})}
      />
    </div>
  </Modal>
{/if}
