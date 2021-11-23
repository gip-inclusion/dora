<script>
  import { page } from "$app/stores";
  import { browser } from "$app/env";
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
  function handleMobilize() {
    orientationModalIsOpen = true;
    if (browser) {
      plausible("mobilisation", {
        props: {
          service: service.name,
          slug: service.slug,
          structure: service.structureInfo.name,
          departement: service.department,
        },
      });
    }
  }
</script>

<style>
  .wrapper {
    position: relative;
    top: 2.5rem;
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

  @screen lg {
    .wrapper {
      position: relative;
      top: -1.5rem;
    }
  }
</style>

<div class="wrapper noprint">
  <div>
    <h3>Mobiliser ce service</h3>
  </div>

  <Label label="Découvrez les modalités prévues pour mobiliser ce service :" />
  <Button on:click={handleMobilize} label="Mobiliser" />

  <OrientationModal {service} bind:isOpen={orientationModalIsOpen} />

  <div class="mt-s16">
    <Field
      type="text"
      label="Partagez cette offre"
      value={sharingUrl}
      vertical
      readonly
    />
  </div>
  {#if !service.isDraft}
    <LinkButton secondary label="Téléchargez le PDF" to={pdfUrl} nofollow />
  {/if}
</div>
