<script lang="ts">
  import { page } from "$app/stores";
  import Button from "$lib/components/display/button.svelte";
  import ServiceContact from "$lib/components/specialized/services/service-contact.svelte";
  import ServiceLoginNotice from "./service-login-notice.svelte";
  import { trackDiMobilisation, trackMobilisation } from "$lib/utils/plausible";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { token } from "$lib/utils/auth";

  export let service;
  export let isDI = false;

  let contactOpen = false;

  export let backgroundColor: "blue" | "white" = "white";

  function handleShowContactClick() {
    contactOpen = true;
    if (isDI) {
      trackDiMobilisation(service, $page.url);
    } else {
      trackMobilisation(service, $page.url);
    }
  }

  const showMobilisation =
    !isDI &&
    service.contactEmail &&
    (service.coachOrientationModes?.includes("envoyer-courriel") ||
      service.coachOrientationModes?.includes("envoyer-fiche-prescription") ||
      service.beneficiariesAccessModes?.includes("envoyer-courriel"));
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
        <div class:text-white={backgroundColor === "blue"}>
          <Button
            on:click={handleShowContactClick}
            extraClass={backgroundColor === "blue"
              ? "!bg-france-blue text-white !border !border-white hover:!bg-magenta-cta hover:!border-france-blue"
              : ""}
            secondary={backgroundColor === "white"}
            label="Voir les informations de contact"
            wFull
          />
        </div>
      {:else}
        <ServiceContact {service} useWhiteText={backgroundColor === "blue"} />
      {/if}

      {#if showMobilisation}
        <div class="mt-s16 mb-s16">
          <LinkButton
            nofollow
            to="/services/{service.slug}/orienter"
            extraClass={backgroundColor === "blue"
              ? "bg-white !text-france-blue hover:!text-white text-center !whitespace-normal text-center"
              : "!whitespace-normal text-center"}
            label="Orienter un ou une bénéficiaire"
            wFull
          />
        </div>
      {/if}
    </div>
  </div>
{:else}
  <ServiceLoginNotice {service} />
{/if}
