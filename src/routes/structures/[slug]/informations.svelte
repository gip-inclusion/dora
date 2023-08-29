<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import DateLabel from "$lib/components/display/date-label.svelte";
  import TextClamp from "$lib/components/display/text-clamp.svelte";
  import {
    computerIcon,
    externalLinkIcon,
    mailLineIcon,
    phoneLineIcon,
    timeLineIcon,
    wheelChairIcon,
  } from "$lib/icons";
  import type {
    StructureMember,
    Structure,
    StructuresOptions,
    PutativeStructureMember,
  } from "$lib/types";
  import { formatPhoneNumber, markdownToHTML } from "$lib/utils/misc";
  import DataInclusionNotice from "./data-inclusion-notice.svelte";
  import QuickStart from "./quick-start.svelte";
  import OsmHours from "$lib/components/specialized/osm-hours.svelte";

  export let structure: Structure;
  export let members: StructureMember[];
  export let putativeMembers: PutativeStructureMember[];
  export let structuresOptions: StructuresOptions;

  let fullDesc;

  $: fullDesc = markdownToHTML(structure.fullDesc, 4);
  $: nationalLabelsDisplay = structure.nationalLabels
    .map((nationalLabel: string) => {
      return structuresOptions.nationalLabels.find(
        (label) => label.value === nationalLabel
      ).label;
    })
    .join(", ");
  $: sourceIsDataInclusion = structure.source?.value.startsWith("di-");
  $: structureHasInfo =
    structure.phone ||
    structure.email ||
    structure.url ||
    structure.openingHours ||
    structure.openingHoursDetails ||
    structure.accesslibreUrl;
</script>

<div class="mb-s40">
  <div
    class="flex flex-col justify-between border-b border-gray-03 pb-s40 sm:flex-row"
  >
    <h2 class="text-france-blue">Présentation de la structure</h2>
    {#if structure.canEditInformations}
      <div class="text-right">
        <LinkButton
          id="update-structure"
          label="Modifier les informations"
          to="/structures/{structure.slug}/editer"
          secondary
        />
      </div>
    {/if}
  </div>
  {#if structure.modificationDate}
    <p class="mt-s40 mb-s0 text-f12 text-gray-dark">
      Informations sur la structure mises à jour le
      <DateLabel date={structure.modificationDate} />
    </p>
  {/if}
  {#if structure.canEditInformations && sourceIsDataInclusion && !structure.hasBeenEdited}
    <div>
      <DataInclusionNotice {structure} />
    </div>
  {/if}
</div>

<div class="structure-body">
  <div class="notice">
    {#if structure.isMember && structure.canEditInformations}
      <QuickStart {structure} {members} {putativeMembers} />
    {/if}
  </div>

  <div class="data">
    <p class="mb-s32 text-f21 font-bold">{structure.shortDesc}</p>

    <div class="flex flex-col gap-s32 md:flex-row">
      {#if nationalLabelsDisplay}
        <div class="flex-1">
          <h3 class="mb-s10 text-f17 text-france-blue">Labels nationaux</h3>
          <p class="m-s0 text-f14">
            {nationalLabelsDisplay}
          </p>
        </div>
      {/if}
      {#if structure.otherLabels}
        <div class="flex-1">
          <h3 class="mb-s10 text-f17 text-france-blue">Autres labels</h3>
          <p class="m-s0 break-all text-f14">{structure.otherLabels}</p>
        </div>
      {/if}
    </div>
  </div>

  {#if fullDesc}
    <hr class="separator" />

    <div class="presentation">
      <TextClamp text={fullDesc} />
    </div>
  {/if}
  {#if structureHasInfo}
    <div class="sidebar">
      <div
        class="flex flex-col gap-s24 rounded-lg border border-gray-02 py-s24 px-s32"
      >
        <h3 class="mb-s8 text-france-blue">Informations pratiques</h3>

        {#if structure.phone}
          <div>
            <h4 class="mb-s8 flex items-center">
              <span class="mr-s8 h-s24 w-s24 fill-current">
                {@html phoneLineIcon}
              </span>
              Téléphone
            </h4>

            <a class="text-gray-text underline" href="tel:{structure.phone}">
              {formatPhoneNumber(structure.phone)}
            </a>
          </div>
        {/if}

        {#if structure.email}
          <div>
            <h4 class="mb-s8 flex items-center">
              <span class="mr-s8 h-s24 w-s24 fill-current">
                {@html mailLineIcon}
              </span>
              E-mail
            </h4>
            <a
              class="break-all text-gray-text  underline"
              href="mailto:{structure.email}">{structure.email}</a
            >
          </div>
        {/if}

        {#if structure.url}
          <div>
            <h4 class="mb-s8 flex items-center">
              <span class="mr-s8 h-s24 w-s24 fill-current">
                {@html computerIcon}
              </span>
              Site web
            </h4>

            <a
              target="_blank"
              title="Ouverture dans une nouvelle fenêtre"
              rel="noopener ugc"
              class="break-all text-gray-text  underline"
              href={structure.url}
            >
              {structure.url}
            </a>
          </div>
        {/if}

        {#if structure.openingHours}
          <div>
            <h4 class="mb-s8 flex items-center">
              <span class="mr-s8 h-s24 w-s24 fill-current">
                {@html timeLineIcon}
              </span>
              Horaires
            </h4>

            <OsmHours osmHours={structure.openingHours} />

            {#if structure.openingHoursDetails}
              <p class="mt-s16 mb-s0 italic text-gray-text">
                <up>*</up>
                {structure.openingHoursDetails}
              </p>
            {/if}
          </div>
        {/if}

        {#if structure.accesslibreUrl}
          <div>
            <h4 class="mb-s8 flex items-center">
              <span class="mr-s8 h-s24 w-s24 fill-current">
                {@html wheelChairIcon}
              </span>
              Accessibilité
            </h4>
            <a
              target="_blank"
              title="Ouverture dans une nouvelle fenêtre"
              rel="noopener ugc"
              class="items-center break-words text-gray-text underline"
              href={structure.accesslibreUrl}
            >
              Retrouvez toutes les infos via ce lien<span
                class="ml-s8 mb-s2 inline-block h-s16 w-s16 justify-end fill-current align-sub"
              >
                {@html externalLinkIcon}
              </span>
            </a>
          </div>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style lang="postcss">
  .notice {
    grid-area: notice;
  }

  .data {
    grid-area: data;
  }

  .separator {
    grid-area: separator;
  }

  .presentation {
    grid-area: presentation;
  }

  .sidebar {
    grid-area: sidebar;
  }

  .structure-body {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 6rem;
    row-gap: 2rem;
    grid-template-areas:
      "notice"
      "data"
      "sidebar"
      "separator"
      "presentation";
  }

  @screen md {
    .structure-body {
      grid-template-columns: 1fr 300px;
      column-gap: 4rem;
      row-gap: 1rem;
      grid-template-areas:
        "notice sidebar"
        "data sidebar"
        "separator sidebar"
        "presentation sidebar";
    }
  }
  @screen lg {
    .structure-body {
      grid-template-columns: 1fr 375px;
    }
  }
</style>
