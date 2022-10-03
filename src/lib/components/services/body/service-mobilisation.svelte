<script>
  import { trackMobilisation } from "$lib/utils/plausible";

  import { token } from "$lib/auth";
  import Button from "$lib/components/button.svelte";
  import ServiceContact from "$lib/components/services/body/service-contact.svelte";
  import ServiceLoginNotice from "$lib/components/services/body/service-login-notice.svelte";

  export let service;
  let contactOpen = false;

  function trackClick() {
    contactOpen = true;
    trackMobilisation(service);
  }

  $: showContact = service?.isContactInfoPublic || $token;
</script>

<h2 class="text-f23">Mobiliser le service</h2>

{#if showContact}
  <div class="noprint w-full sm:w-auto">
    {#if !contactOpen}
      <div class="mb-s16">
        <Button
          on:click={trackClick}
          label="Voir les informations de contact"
          wFull
        />
      </div>
    {:else}
      <ServiceContact {service} />
    {/if}
  </div>
{:else}
  <ServiceLoginNotice {service} />
{/if}
