<script>
  import { page } from "$app/stores";
  import { token } from "$lib/auth";
  import Button from "$lib/components/button.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import { PDF_SERVICE_URL } from "$lib/env";
  import OrientationModal from "./_orientation-modal.svelte";

  export let service;

  export let sharingUrl = `https://${$page.host}${$page.path}`;
  export let pdfUrl = `${PDF_SERVICE_URL}/service-pdf/${service.slug}`;

  let orientationModalIsOpen = false;
</script>

<style>
  .wrapper {
    position: relative;
    top: -4rem;
    display: flex;
    flex-direction: column;
    padding: var(--s32);
    border: 3px solid var(--col-gray-dark);
    margin-right: auto;
    margin-left: auto;
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-md);
    gap: var(--s16);
    text-align: left;
  }
</style>

<div class="wrapper noprint">
  <div>
    <h3>Mobiliser ce service</h3>
  </div>

  {#if !$token}
    <Label
      label="Vous devez être connecté•e pour accéder aux informations de contact et mobiliser ce service pour votre bénéficiaire." />
    <LinkButton
      label="Connexion"
      to={`/auth/connexion?next=${encodeURIComponent($page.path)}`} />
  {:else}
    <Label
      label="Découvrez les modalités prévues pour mobiliser ce service :" />
    <Button
      on:click={() => (orientationModalIsOpen = true)}
      label="Mobiliser" />
  {/if}

  <OrientationModal {service} bind:isOpen={orientationModalIsOpen} />

  <div class="mt-2">
    <Field
      type="text"
      label="Partagez cette offre"
      value={sharingUrl}
      vertical
      readonly />
  </div>
  {#if !service.isDraft}
    <LinkButton secondary label="Téléchargez le PDF" to={pdfUrl} />
  {/if}
</div>
