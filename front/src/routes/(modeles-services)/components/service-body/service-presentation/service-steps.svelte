<script lang="ts">
  import { page } from "$app/state";

  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import Linkify from "$lib/components/display/linkify.svelte";
  import type { ModesMobilisation, Model, Service } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";

  import ServiceList from "./components/service-list.svelte";
  import ServiceSection from "./components/service-section.svelte";
  import ServiceSubsection from "./components/service-subsection.svelte";

  interface Props {
    service: Service | Model;
    onTrackMobilisation: (url?: string) => void;
  }

  let { service, onTrackMobilisation }: Props = $props();

  const orderedModesMobilisationValues: Record<ModesMobilisation, number> = {
    "formulaire-dora": 0,
    "utiliser-lien-mobilisation": 1,
    "envoyer-un-courriel": 2,
    telephoner: 3,
    "se-presenter": 4,
  };

  let isDI = $derived("source" in service);
  // Passe le `searchId` (dans l'URL) vers le détail de la structure afin de
  // lier la consultation à la recherche originale.
  let searchId = $derived(page.url.searchParams.get("searchId"));

  let modesMobilisationValueAndDisplay = $derived(
    (service.modesMobilisation ?? [])
      .map((val, index) => [val, service.modesMobilisationDisplay?.[index]])
      .sort(
        (a, b) =>
          orderedModesMobilisationValues[a[0]] -
          orderedModesMobilisationValues[b[0]]
      )
  );

  let mobilisableParDisplay = $derived(
    (service.mobilisableParDisplay ?? []).join(", ")
  );
</script>

<ServiceSection title="Les démarches à réaliser">
  <ServiceSubsection
    title={mobilisableParDisplay
      ? `Mobilisable par : ${mobilisableParDisplay}`
      : "Comment mobiliser ce service"}
  >
    <ServiceList>
      {#each modesMobilisationValueAndDisplay as [modeValue, modeDisplay] (modeValue)}
        <li>
          {#if modeValue === "formulaire-dora"}
            Orienter votre bénéficiaire via le formulaire DORA
          {:else if modeValue === "utiliser-lien-mobilisation"}
            <a
              href={service.lienMobilisation}
              target="_blank"
              onclick={() =>
                onTrackMobilisation(service.lienMobilisation ?? undefined)}
              class="text-magenta-cta underline"
              >Faire une demande<ExternalLinkIcon /></a
            >
          {:else}
            {modeDisplay}
          {/if}
        </li>
      {:else}
        <li>Non renseigné</li>
      {/each}
    </ServiceList>

    {#if service.mobilisationPrecisions}
      <div class="mt-s16">
        <Linkify
          text={service.mobilisationPrecisions}
          onLinkClick={onTrackMobilisation}
        />
      </div>
    {/if}

    {#if !$userInfo && !isDI}
      <div class="mt-s16">
        <strong
          >Vous étes un particulier&#8239;? <a
            class="text-magenta-cta underline"
            href="/structures/{service.structureInfo.slug}{searchId
              ? `?searchId=${searchId}`
              : ''}">Voir les coordonnées de la structure</a
          ></strong
        >
      </div>
    {/if}
  </ServiceSubsection>
</ServiceSection>
