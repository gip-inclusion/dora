<script>
  import { trackMobilisation } from "$lib/utils/plausible";

  import Button from "$lib/components/button.svelte";
  import ServiceContact from "$lib/components/services/body/service-contact.svelte";
  import ServiceLoginNotice from "$lib/components/services/body/service-login-notice.svelte";

  export let service, showContact;
  let contactOpen = false;

  function trackClick() {
    contactOpen = true;
    trackMobilisation(service);
  }
</script>

<h2 class="text-f23">Mobiliser le service</h2>

{#if showContact}
  <div class="w-full sm:w-auto">
    <div class="hidden print:inline">
      <ServiceContact {service} />
    </div>
    <div class="print:hidden">
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
  </div>
{:else}
  <ServiceLoginNotice {service} />
{/if}
