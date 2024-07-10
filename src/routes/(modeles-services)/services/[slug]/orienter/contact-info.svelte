<script lang="ts">
  import type { Service } from "$lib/types";
  import { trackMobilisation } from "$lib/utils/stats";
  import Button from "$lib/components/display/button.svelte";
  import ContactEmail from "$lib/components/specialized/services/contact-email.svelte";
  import ContactPhone from "$lib/components/specialized/services/contact-phone.svelte";
  import { page } from "$app/stores";
  import { getContext } from "svelte";

  export let service: Service;
  export let isDI: boolean;

  const shouldTrack = Boolean(getContext("shouldTrack"));

  let contactBoxOpen = false;

  function handleShowContactClick() {
    contactBoxOpen = true;
    // tracking comme MER uniquement :
    // - pour les services avec infos de contact publiques
    // - ET si on ne se trouve pas déjà dans le parcours du formulaire d'orientation (shouldTrack=true)
    if (service.isContactInfoPublic && shouldTrack) {
      trackMobilisation(service, $page.url, isDI);
    }
  }
</script>

{#if contactBoxOpen}
  <div class="flex flex-col gap-s4">
    {#if service.contactName}
      <p class="mb-s6 mr-s24 text-f17 text-gray-dark">
        <strong>{service.contactName}</strong>
      </p>
    {/if}
    {#if service.contactPhone}
      <ContactPhone {service} />
    {/if}
    <ContactEmail {service} />
  </div>
{:else}
  <Button
    label="Afficher les informations de contact"
    on:click={handleShowContactClick}
  />
{/if}
