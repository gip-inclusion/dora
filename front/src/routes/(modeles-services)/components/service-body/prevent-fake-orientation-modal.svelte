<script lang="ts">
  import { browser } from "$app/environment";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { URL_DOCUMENTATION_ORIENTATION } from "$lib/consts";

  interface Props {
    isOpen?: boolean;
    orientationFormUrl: string;
    onShowVideo: () => void;
    onTrackMobilisation: () => void;
  }

  let {
    isOpen = $bindable(false),
    orientationFormUrl,
    onShowVideo,
    onTrackMobilisation,
  }: Props = $props();
</script>

{#if browser}
  <Modal bind:isOpen title="Avant de continuer" width="medium">
    <p>
      ⚠️ <strong>Rappel :</strong> Les orientations fictives, destinées à tester l’outil,
      nécessitent une vérification manuelle, ajoutant une charge de travail pour nos
      équipes.
    </p>
    <p>
      Nous vous invitons à consulter notre <a
        href={URL_DOCUMENTATION_ORIENTATION}
        target="_blank"
        class="text-magenta-cta underline">documentation</a
      > ou voir la vidéo de présentation pour comprendre l’utilisation du formulaire
      d’orientation.
    </p>
    {#snippet footer()}
      <div class="gap-s12 flex justify-end">
        <LinkButton
          label="Poursuivre l’orientation"
          secondary
          to={orientationFormUrl}
          onclick={onTrackMobilisation}
        />
        <Button label="Regarder la vidéo" onclick={onShowVideo} />
      </div>
    {/snippet}
  </Modal>
{/if}
