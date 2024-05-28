<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import { refreshOrientationLink } from "$lib/utils/orientation";

  export let queryId: string;

  let emailSent = false;

  function sendNewLink() {
    refreshOrientationLink(queryId);
    emailSent = true;
  }
</script>

{#if emailSent}
  <Notice
    type="info"
    title="Un nouveau lien vers cette orientation vous a été envoyé"
  >
    Vérifiez le contenu de votre boîte e-mail. Le nouveau lien à une validité de
    7 jours.
  </Notice>
{:else}
  <Notice
    type="warning"
    title="Le lien vers la demande d'orientation a expiré..."
  >
    Le lien qui vous a été communiqué par e-mail avait une durée de validité de
    7 jours et est maintenant expiré.
  </Notice>

  <div class="p-s24 text-center">
    <p class="text-f16">
      Vous pouvez recevoir un nouvel e-mail de demande d'orientation contenant
      un lien valide en cliquant sur le bouton ci-dessous.
    </p>
    <Button
      label="Envoyer un nouveau lien par e-mail"
      extraClass="mt-s16"
      on:click={sendNewLink}
    />
  </div>
{/if}
