<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import ServiceContact from "$lib/components/specialized/services/display/service-contact.svelte";
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";
  import type { Service } from "$lib/types";
  import { getToken } from "$lib/utils/auth";

  import SharingModal from "../sharing-modal.svelte";

  interface Props {
    service: Service;
    isDI?: boolean;
    orientationFormUrl: string;
    handleOrientationFormClickEvent: (event: MouseEvent) => void;
    onTrackMobilisation: (url?: string) => void;
  }

  let {
    service,
    isDI = false,
    orientationFormUrl,
    handleOrientationFormClickEvent,
    onTrackMobilisation,
  }: Props = $props();

  let isOrientableWithDoraForm = $derived(
    (service.isOrientable &&
      service.coachOrientationModes?.includes("formulaire-dora")) ||
      service.isOrientableFtService
  );
  let hasExternalForm = $derived(
    service.coachOrientationModes?.includes("completer-le-formulaire-dadhesion")
  );

  let sharingModalIsOpen = $state(false);
  let contactBoxOpen = $state(false);

  function handleShowContactClick() {
    if (!getToken() && !service.isContactInfoPublic) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
      return;
    }
    contactBoxOpen = true;
    // on tracke comme une MER si les contacts du service sont publics
    onTrackMobilisation();
  }

  function handleExternalFormClick(externalUrl: string) {
    onTrackMobilisation(externalUrl);
  }

  function handleShareClick() {
    sharingModalIsOpen = true;
  }
</script>

<SharingModal bind:isOpen={sharingModalIsOpen} {service} {isDI} />

<h2 class="text-f23 text-white">Mobiliser ce service</h2>

<div class="mt-s16 gap-s16 flex w-full flex-col sm:w-auto print:hidden">
  {#if !(isDI && hasExternalForm)}
    {#if isOrientableWithDoraForm}
      <LinkButton
        label="Orienter votre bénéficiaire"
        to={orientationFormUrl}
        extraClass="bg-white text-france-blue! hover:text-white!"
        onclick={handleOrientationFormClickEvent}
      />
    {:else if service.contactInfoFilled}
      {#if !contactBoxOpen}
        <Button
          onclick={handleShowContactClick}
          extraClass="mt-s16 bg-white text-france-blue! hover:text-white! text-center whitespace-normal! text-center"
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
      onclick={() =>
        handleExternalFormClick(service.coachOrientationModesExternalFormLink)}
      to={service.coachOrientationModesExternalFormLink}
      extraClass="bg-white text-france-blue! hover:text-white! text-center whitespace-normal! text-center"
      label={service.coachOrientationModesExternalFormLinkText ||
        "Orienter votre bénéficiaire"}
      icon={ExternalLinkLineSystem}
      iconOnRight
      otherTab
      wFull
    />
  {/if}

  <Button
    onclick={handleShareClick}
    extraClass="bg-france-blue! text-white border! border-white! hover:bg-magenta-cta! hover:border-france-blue!"
    label="Partager cette fiche"
    wFull
  />
</div>
