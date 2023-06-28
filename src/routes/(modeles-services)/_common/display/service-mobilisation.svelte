<script lang="ts">
  import { page } from "$app/stores";
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
    trackMobilisation(service, $page.url);
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
            extraClass={backgroundColor === "blue"
              ? "bg-white !text-france-blue hover:!text-white"
              : ""}
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
