<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import ServiceContact from "$lib/components/specialized/services/service-contact.svelte";
  import ServiceLoginNotice from "./service-login-notice.svelte";
  import { trackMobilisation } from "$lib/utils/plausible";
  import { token } from "$lib/utils/auth";

  export let service;
  let contactOpen = false;

  export let backgroundColor: "blue" | "white" = "white";

  function trackClick() {
    contactOpen = true;
    trackMobilisation(service);
  }
</script>

<h2 class="text-f23" class:text-white={backgroundColor === "blue"}>
  Mobiliser le service
</h2>

{#if $token}
  <div class="w-full sm:w-auto">
    <div class="hidden print:inline">
      <ServiceContact {service} />
    </div>
    <div class="print:hidden">
      {#if !contactOpen}
        <div class="mb-s16" class:text-white={backgroundColor === "blue"}>
          <Button
            on:click={trackClick}
            label="Voir les informations de contact"
            wFull
          />
        </div>
      {:else}
        <ServiceContact {service} useWhiteText={backgroundColor === "blue"} />
      {/if}
    </div>
  </div>
{:else}
  <ServiceLoginNotice {service} />
{/if}
