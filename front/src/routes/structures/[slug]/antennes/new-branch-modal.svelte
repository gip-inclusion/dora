<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import { URL_HELP_SITE } from "$lib/consts";

  interface Props {
    isOpen?: boolean;
  }

  let { isOpen = $bindable(false) }: Props = $props();
</script>

{#if isOpen}
  <Modal bind:isOpen title="Créer une ou plusieurs antennes" width="medium">
    <p class="text-f16">
      Pour demander la création d’une ou plusieurs antennes, il suffit
      simplement de nous en faire la demande via notre chatbot (bouton “Discuter
      avec nous” en bas de la page <a
        href={`${URL_HELP_SITE}`}
        class="text-magenta-cta underline"
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener">{URL_HELP_SITE}</a
      >).
    </p>

    <p class="text-f16">
      Vous aurez besoin de vous munir du nom de cette nouvelle structure et du
      lien vers la structure mère sur DORA.
    </p>

    <p class="text-f16">
      Si votre antenne a un numéro SIRET différent de la structure mère, vous
      pouvez directement créer l’antenne en cliquant sur le bouton "Adhérer à
      une structure" (bouton se trouvant dans le menu déroulant de vos
      structures d’appartenance - dans l’en-tête du site DORA).
    </p>
  </Modal>
{/if}
