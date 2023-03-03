<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
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
  import { isStructureInformationsComplete } from "$lib/requests/structures";
  import type { Structure, StructuresOptions } from "$lib/types";
  import { formatPhoneNumber, markdownToHTML } from "$lib/utils/misc";
  import { formatOsmHours } from "$lib/utils/opening-hours";
  import DataInclusionNotice from "./data-inclusion-notice.svelte";

  export let structure: Structure;
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
    <h2 class="text-france-blue">Informations</h2>
    {#if structure.canWrite}
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
  {#if structure.canWrite && sourceIsDataInclusion && !structure.hasBeenEdited}
    <div>
      <DataInclusionNotice {structure} />
    </div>
  {/if}
</div>

<div class="structure-body">
  <div class="notice">
    {#if structure.canWrite}
      {#if !isStructureInformationsComplete(structure) && !(sourceIsDataInclusion && !structure.hasBeenEdited)}
        <Notice
          title="Les informations de votre structure ne sont pas complètes"
          type="warning"
          showIcon={false}
        >
          <div class="flex flex-col">
            <p class="mb-s24 text-f14">
              En complétant votre fiche, vous gagnerez en visibilité auprès des
              acteurs locaux et régionaux.
            </p>
            <p>
              <LinkButton
                to={`/structures/${structure.slug}/editer`}
                label="Mettre à jour"
                small
              />
            </p>
          </div>
        </Notice>
      {/if}
    {/if}
  </div>

  <div class="data">
    <p class="bold mb-s32 text-f21">{structure.shortDesc}</p>

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
      <h3 class="text-f32 leading-32 text-france-blue md:mt-s32">
        Présentation de la structure
      </h3>
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
              rel="noopener nofollow"
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

            <ul class="text-f16">
              {#each formatOsmHours(structure.openingHours) as [prefix, hourStr]}
                <li class="mb-s8 flex items-center text-gray-text">
                  <span class="mr-s16 w-s35">{prefix}</span>
                  <span>{hourStr}</span>
                </li>
              {/each}
            </ul>

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
              rel="noopener nofollow"
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
