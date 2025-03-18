<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import Linkify from "$lib/components/display/linkify.svelte";
  import type {
    BeneficiaryAccessModes,
    CoachOrientationModes,
    Model,
    Service,
  } from "$lib/types";

  import ServiceList from "./components/service-list.svelte";
  import ServiceSection from "./components/service-section.svelte";
  import ServiceSubsection from "./components/service-subsection.svelte";

  export let service: Service | Model;

  const orderedCoachOrientationModeValues: Record<
    CoachOrientationModes,
    number
  > = {
    "formulaire-dora": 0,
    "envoyer-un-mail-avec-une-fiche-de-prescription": 1,
    "completer-le-formulaire-dadhesion": 2,
    "envoyer-un-mail": 3,
    telephoner: 4,
    autre: 5,
  };

  const orderedBeneficiariesAccessModeValues: Record<
    BeneficiaryAccessModes,
    number
  > = {
    "se-presenter": 0,
    "completer-le-formulaire-dadhesion": 1,
    "envoyer-un-mail": 2,
    telephoner: 3,
    professionnel: 4,
    autre: 5,
  };

  const dispatch = createEventDispatcher<{
    trackMobilisation: { externalUrl?: string };
  }>();

  function trackMobilisationUnconditionally(externalUrl: string) {
    dispatch("trackMobilisation", { externalUrl });
  }

  $: isDI = "source" in service;

  $: coachOrientationModesValueAndDisplay = (
    service.coachOrientationModes ?? []
  )
    .map((val, index) => [val, service.coachOrientationModesDisplay[index]])
    .sort(
      (a, b) =>
        orderedCoachOrientationModeValues[a[0]] -
        orderedCoachOrientationModeValues[b[0]]
    );

  $: beneficiariesAccessModesValueAndDisplay = (
    service.beneficiariesAccessModes ?? []
  )
    .map((val, index) => [val, service.beneficiariesAccessModesDisplay[index]])
    .sort(
      (a, b) =>
        orderedBeneficiariesAccessModeValues[a[0]] -
        orderedBeneficiariesAccessModeValues[b[0]]
    );
</script>

<ServiceSection title="Les démarches à réaliser">
  <ServiceSubsection title="Pour les professionnels de l’accompagnement">
    <ServiceList>
      {#each coachOrientationModesValueAndDisplay as [modeValue, modeDisplay] (modeValue)}
        <li>
          {#if modeValue === "formulaire-dora"}
            Orienter votre bénéficiaire via le formulaire DORA
          {:else if modeValue === "envoyer-un-mail-avec-une-fiche-de-prescription" && "contactEmail" in service}
            Envoyer un email avec une fiche de prescription
          {:else if modeValue === "autre"}
            <Linkify
              text={service.coachOrientationModesOther}
              on:linkClick={(event) =>
                trackMobilisationUnconditionally(event.detail.url)}
            />
          {:else}
            {modeDisplay}
          {/if}
        </li>
      {:else}
        <li>Non renseigné</li>
      {/each}
    </ServiceList>
  </ServiceSubsection>
  <ServiceSubsection title="Pour les particuliers">
    <ServiceList>
      {#each beneficiariesAccessModesValueAndDisplay as [modeValue, modeDisplay] (modeValue)}
        <li>
          {#if modeValue === "completer-le-formulaire-dadhesion"}
            <a
              href={service.beneficiariesAccessModesExternalFormLink}
              target="_blank"
              on:click={() =>
                trackMobilisationUnconditionally(
                  service.beneficiariesAccessModesExternalFormLink
                )}
              class="text-magenta-cta underline"
              >{service.beneficiariesAccessModesExternalFormLinkText ||
                "Faire une demande"}<ExternalLinkIcon /></a
            >
          {:else if modeValue === "professionnel"}
            Orientation par un professionnel
          {:else if modeValue === "autre"}
            <Linkify
              text={service.beneficiariesAccessModesOther}
              on:linkClick={(event) =>
                trackMobilisationUnconditionally(event.detail.url)}
            />
          {:else}
            {modeDisplay}
          {/if}
        </li>
      {:else}
        <li>Non renseigné</li>
      {/each}
    </ServiceList>
    {#if !isDI}
      <div class="mt-s16">
        <strong
          >Vous étes un particulier&#8239;? <a
            class="text-magenta-cta underline"
            href="/structures/{service.structureInfo.slug}"
            >Voir les coordonnées de la structure</a
          ></strong
        >
      </div>
    {/if}
  </ServiceSubsection>
</ServiceSection>
