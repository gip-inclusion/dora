<script lang="ts">
  import { page } from "$app/stores";
  import { userInfo } from "$lib/utils/auth";

  import Button from "$lib/components/display/button.svelte";
  import ServiceContact from "$lib/components/specialized/services/service-contact.svelte";
  import ServiceLoginNotice from "./service-login-notice.svelte";
  import { trackDiMobilisation, trackMobilisation } from "$lib/utils/plausible";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { token } from "$lib/utils/auth";

  export let service;
  export let isDI = false;

  let contactOpen = false;

  function handleShowContactClick() {
    contactOpen = true;
    if (isDI) {
      trackDiMobilisation(service, $page.url);
    } else {
      trackMobilisation(service, $page.url);
    }
  }
</script>

<h2 class="text-f23 text-white">Mobiliser le service</h2>

{#if $token}
  {#if !$userInfo.structures.length}
    <div class="mb-s8 italic">
      {#if $userInfo.pendingStructures.length === 1}
        Le temps que votre adhésion à la structure “{$userInfo
          .pendingStructures[0].name}” soit validée, vous ne pouvez pas
        visualiser ces informations.{:else}Le temps que vos demandes d’adhésion
        soient validées, vous ne pouvez pas visualiser ces informations.{/if}
    </div>
  {:else}
    <div class="w-full sm:w-auto">
      <div class="hidden print:inline">
        <ServiceContact {service} />
      </div>
      <div class="print:hidden">
        {#if !contactOpen}
          <div class="text-white">
            <Button
              on:click={handleShowContactClick}
              extraClass="!bg-france-blue text-white !border !border-white hover:!bg-magenta-cta hover:!border-france-blue"
              label="Voir les informations de contact"
              wFull
            />
          </div>
        {:else}
          <ServiceContact {service} />
        {/if}

        {#if service.isOrientable}
          <div class="mb-s16 mt-s16">
            <LinkButton
              nofollow
              to="/services/{service.slug}/orienter"
              extraClass="bg-white !text-france-blue hover:!text-white text-center !whitespace-normal text-center"
              label="Orienter un ou une bénéficiaire"
              wFull
            />
          </div>
        {/if}
      </div>
    </div>
  {/if}
{:else}
  <ServiceLoginNotice {service} />
{/if}
