<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { token } from "$lib/utils/auth";

  import Button from "$lib/components/display/button.svelte";
  import ServiceContact from "$lib/components/specialized/services/service-contact.svelte";
  import { trackMobilisation } from "$lib/utils/stats";
  import type { Service } from "$lib/types";
  import SharingModal from "./modals/sharing-modal.svelte";

  export let service: Service;
  // Si il n'y a pas d'information de contact, on n'affiche pas le bouton
  export let contactBoxOpen = !(service.contactEmail || service.contactPhone);
  export let isDI = false;

  let sharingModalIsOpen = false;
  function showContact() {
    if (!$token) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
      return;
    }
    contactBoxOpen = true;
    trackMobilisation(service, $page.url, isDI);
  }

  function handleOrientationClick() {
    if (!service.isOrientable) {
      showContact();
    } else {
      if ($token) {
        trackMobilisation(service, $page.url, isDI);
      }
      const searchId = $page.url.searchParams.get("searchId");
      const searchFragment = searchId ? `?searchId=${searchId}` : "";
      goto(
        `/services/${isDI ? "di--" : ""}${
          service.slug
        }/orienter${searchFragment}`
      );
    }
  }

  function handleShareClick() {
    sharingModalIsOpen = true;
  }
</script>

<SharingModal bind:isOpen={sharingModalIsOpen} {service} {isDI} />

<h2 class="text-f23 text-white">Mobiliser ce service</h2>

<div class="w-full sm:w-auto">
  <div class="print:hidden">
    <div class="mb-s16 mt-s16">
      {#if contactBoxOpen}
        <ServiceContact {service} />
      {:else}
        <Button
          on:click={handleOrientationClick}
          extraClass="bg-white !text-france-blue hover:!text-white text-center !whitespace-normal text-center"
          label="Orienter votre bénéficiaire"
          wFull
        />
      {/if}
    </div>

    <div class="text-white">
      <Button
        on:click={handleShareClick}
        extraClass="!bg-france-blue text-white !border !border-white hover:!bg-magenta-cta hover:!border-france-blue"
        label="Partager cette fiche"
        wFull
      />
    </div>
  </div>
</div>
