<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import ServiceContact from "$lib/components/specialized/services/display/service-contact.svelte";
  import { externalLinkIcon } from "$lib/icons";
  import type { Service } from "$lib/types";
  import { token } from "$lib/utils/auth";

  import SharingModal from "./modals/sharing-modal.svelte";

  export let service: Service;
  export let isDI = false;

  $: isOrientasbleWithDoraForm =
    service.isOrientable &&
    service.coachOrientationModes?.includes("formulaire-dora");
  $: hasExternalForm = service.coachOrientationModes?.includes(
    "completer-le-formulaire-dadhesion"
  );

  const dispatch = createEventDispatcher<{
    trackMobilisation: { externalUrl?: string };
  }>();

  let sharingModalIsOpen = false;
  let contactBoxOpen = false;

  function showContact() {
    if (!$token && !service.isContactInfoPublic) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
      return;
    }
    contactBoxOpen = true;
    // on tracke comme une MER si les contacts du service sont publics
    dispatch("trackMobilisation", {});
  }

  function handleOrientationClick() {
    if (!isOrientasbleWithDoraForm) {
      showContact();
    } else {
      if ($token) {
        dispatch("trackMobilisation", {});
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

  function handleExternalFormClick(externalUrl: string) {
    dispatch("trackMobilisation", { externalUrl });
  }

  function handleShareClick() {
    sharingModalIsOpen = true;
  }
</script>

<SharingModal bind:isOpen={sharingModalIsOpen} {service} {isDI} />

<h2 class="text-f23 text-white">Mobiliser ce service</h2>

<div class="mt-s16 flex w-full flex-col gap-s16 sm:w-auto print:hidden">
  {#if !(isDI && hasExternalForm)}
    {#if isOrientasbleWithDoraForm || service.contactInfoFilled}
      {#if !contactBoxOpen}
        <Button
          on:click={handleOrientationClick}
          extraClass="mt-s16 bg-white !text-france-blue hover:!text-white text-center !whitespace-normal text-center"
          label="Orienter votre bénéficiaire"
          wFull
        />
      {:else}
        <ServiceContact {service} />
      {/if}
    {:else}
      Informations de contact non renseignées
    {/if}
  {/if}

  {#if hasExternalForm}
    <LinkButton
      on:click={() =>
        handleExternalFormClick(service.coachOrientationModesExternalFormLink)}
      to={service.coachOrientationModesExternalFormLink}
      extraClass="bg-white !text-france-blue hover:!text-white text-center !whitespace-normal text-center"
      label={service.coachOrientationModesExternalFormLinkText ||
        "Orienter votre bénéficiaire"}
      icon={externalLinkIcon}
      iconOnRight
      otherTab
      wFull
    />
  {/if}

  <Button
    on:click={handleShareClick}
    extraClass="!bg-france-blue text-white !border !border-white hover:!bg-magenta-cta hover:!border-france-blue"
    label="Partager cette fiche"
    wFull
  />
</div>
