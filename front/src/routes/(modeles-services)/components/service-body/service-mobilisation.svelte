<script lang="ts">
  import { page } from "$app/stores";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import ServiceContact from "$lib/components/specialized/services/display/service-contact.svelte";
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";
  import type { Service } from "$lib/types";
  import { isAuthenticated } from "$lib/utils/auth";
  import { buildServiceShareMailto } from "$lib/utils/service-share-mailto";
  import { trackMatomoEvent } from "$lib/utils/matomo";

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

  let contactBoxOpen = $state(false);

  let shareMailtoHref = $derived(buildServiceShareMailto(service, isDI));

  let loginHref = $derived(
    `/auth/connexion?next=${encodeURIComponent(
      $page.url.pathname + $page.url.search
    )}`
  );

  let structureHref = $derived(`/structures/${service.structureInfo.slug}`);

  function handleShowContactClick() {
    contactBoxOpen = true;
    onTrackMobilisation();
  }

  function handleExternalFormClick(externalUrl: string) {
    onTrackMobilisation(externalUrl);
  }

  function handleShareClick() {
    trackMatomoEvent({
      category: "Page Service",
      action: "Clic Bouton Partager cette Fiche",
      name: $page.url.pathname,
    });
  }
</script>

<h2 class="text-f23 text-white">Mobiliser ce service</h2>

<div class="mt-s16 gap-s16 flex w-full flex-col sm:w-auto print:hidden">
  {#if service.isOrientable && !(isDI && service.mobilisationLink)}
    <LinkButton
      label="Orienter votre bénéficiaire"
      to={orientationFormUrl}
      extraClass="bg-white text-france-blue! hover:text-white!"
      onclick={handleOrientationFormClickEvent}
    />
  {:else if service.mobilisationLink}
    {@const externalFormLink = service.mobilisationLink}
    <LinkButton
      onclick={() => handleExternalFormClick(externalFormLink)}
      to={externalFormLink}
      extraClass="bg-white text-france-blue! hover:text-white! text-center whitespace-normal! text-center"
      label={"Orienter votre bénéficiaire"}
      icon={ExternalLinkLineSystem}
      iconOnRight
      otherTab
      wFull
    />
  {/if}

  {#if !contactBoxOpen}
    <Button
      onclick={handleShowContactClick}
      extraClass="bg-white text-france-blue! hover:text-white! text-center whitespace-normal! text-center"
      label="Afficher les données de contact"
      wFull
    />
  {:else}
    {#if service.contactInfoFilled && (service.isContactInfoPublic || isAuthenticated())}
      <ServiceContact {service} />
    {:else}
      <div class="p-s16 gap-s4 flex flex-col bg-white/20 text-white">
        <h3 class="text-f18 font-bold text-white">Données de contact</h3>
        {#if service.contactInfoFilled && !service.isContactInfoPublic && !isAuthenticated()}
          <span class="text-f16">
            <a href={loginHref} class="font-bold underline"
              >Connectez-vous à Dora</a
            > pour afficher le contact du service
          </span>
          <span class="text-f16">ou</span>
          <span class="text-f16">
            <a href={structureHref} class="font-bold underline"
              >Contactez la structure</a
            >
          </span>
        {:else}
          <span class="text-f16">
            Il n'y a pas de données de contact dédiées à ce service. Nous vous
            invitons à
            <a href={structureHref} class="font-bold underline"
              >contacter la structure</a
            >
          </span>
        {/if}
      </div>
    {/if}
  {/if}

  <LinkButton
    onclick={handleShareClick}
    to={shareMailtoHref}
    extraClass="bg-france-blue! text-white border! border-white! hover:bg-magenta-cta! hover:border-france-blue!"
    label="Partager cette fiche"
    wFull
  />
</div>
