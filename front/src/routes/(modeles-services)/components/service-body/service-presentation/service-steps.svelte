<script lang="ts">
  import { page } from "$app/state";

  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import Linkify from "$lib/components/display/linkify.svelte";
  import type { Model, Service } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { usesDoraForm } from "$lib/utils/service";

  import ServiceList from "./components/service-list.svelte";
  import ServiceSection from "./components/service-section.svelte";
  import ServiceSubsection from "./components/service-subsection.svelte";

  interface Props {
    service: Service | Model;
    onTrackMobilisation: (url?: string) => void;
  }

  let { service, onTrackMobilisation }: Props = $props();

  let isDI = $derived("source" in service);
  // Passe le `searchId` (dans l'URL) vers le détail de la structure afin de
  // lier la consultation à la recherche originale.
  let searchId = $derived(page.url.searchParams.get("searchId"));
  let hasProfessionnels = $derived(
    !!service.mobilisableBy?.includes("professionnels")
  );
  let hasUsagers = $derived(!!service.mobilisableBy?.includes("usagers"));
  let modeEntries = $derived(
    (service.mobilisationModes ?? []).map((val, index) => [
      val,
      service.mobilisationModesDisplay?.[index],
    ])
  );
</script>

<ServiceSection title="Les démarches à réaliser">
  <ServiceSubsection title="Pour les professionnels de l’accompagnement">
    <ServiceList>
      {#if hasProfessionnels && (modeEntries.length || service.mobilisationDetails)}
        {#each modeEntries as [modeValue, modeDisplay] (modeValue)}
          <li>
            {#if modeValue === "utiliser-lien-mobilisation" && usesDoraForm(service)}
              Orienter votre bénéficiaire via le formulaire DORA
            {:else if modeValue === "utiliser-lien-mobilisation" && service.mobilisationLink}
              <a
                href={service.mobilisationLink}
                target="_blank"
                onclick={() => onTrackMobilisation(service.mobilisationLink)}
                class="text-magenta-cta underline"
                >Faire une demande<ExternalLinkIcon /></a
              >
            {:else}
              {modeDisplay}
            {/if}
          </li>
        {/each}
        {#if service.mobilisationDetails}
          <li>
            <Linkify
              text={service.mobilisationDetails}
              onLinkClick={onTrackMobilisation}
            />
          </li>
        {/if}
      {:else}
        <li>Non renseigné</li>
      {/if}
    </ServiceList>
  </ServiceSubsection>
  <ServiceSubsection title="Pour les particuliers">
    <ServiceList>
      {#if hasUsagers && (modeEntries.length || service.mobilisationDetails)}
        {#each modeEntries as [modeValue, modeDisplay] (modeValue)}
          <li>
            {#if modeValue === "utiliser-lien-mobilisation" && usesDoraForm(service)}
              Orienter votre bénéficiaire via le formulaire DORA
            {:else if modeValue === "utiliser-lien-mobilisation" && service.mobilisationLink}
              <a
                href={service.mobilisationLink}
                target="_blank"
                onclick={() => onTrackMobilisation(service.mobilisationLink)}
                class="text-magenta-cta underline"
                >Faire une demande<ExternalLinkIcon /></a
              >
            {:else}
              {modeDisplay}
            {/if}
          </li>
        {/each}
        {#if service.mobilisationDetails}
          <li>
            <Linkify
              text={service.mobilisationDetails}
              onLinkClick={onTrackMobilisation}
            />
          </li>
        {/if}
      {:else}
        <li>Non renseigné</li>
      {/if}
    </ServiceList>
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
