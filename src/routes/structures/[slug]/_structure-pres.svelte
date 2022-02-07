<script>
  import { token } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import {
    computerIcon,
    externalLineIcon,
    mailIcon,
    mapPinIcon,
    phoneIcon,
  } from "$lib/icons";

  export let structure;

  const editLink = `/tableau-de-bord/structures/${structure.slug}/editer`;
</script>

<div class="col-span-full flex flex-col gap-s16 lg:col-start-1 lg:col-end-5">
  <div
    class=" mt-s64 flex flex-row flex-wrap gap-x-s24 text-f14 text-gray-text lg:flex-col lg:gap-s8"
  >
    <div class="icon-label">
      <div class="icon">
        {@html mapPinIcon}
      </div>
      <div>
        <p>{structure.address1}</p>
        {#if structure.address2}
          <div>{structure.address2}</div>
        {/if}
        <div>{structure.postalCode} {structure.city}</div>
      </div>
    </div>

    {#if structure.url}
      <div class="icon-label">
        <div class="icon">
          {@html computerIcon}
        </div>
        <a target="_blank" rel="noopener nofollow" href={structure.url}>
          {structure.url}
        </a>
        <div class="ext-icon">
          {@html externalLineIcon}
        </div>
      </div>
    {/if}
    {#if structure.email}
      <div class="icon-label">
        <div class="icon">
          {@html mailIcon}
        </div>

        <a href="mailto:{structure.email}">
          {structure.email}
        </a>
        <div class="ext-icon">
          {@html externalLineIcon}
        </div>
      </div>
    {/if}
    <div class="icon-label">
      <div class="icon">
        {@html phoneIcon}
      </div>
      <a href="tel:{structure.phone}">
        {structure.phone}
      </a>
    </div>
  </div>
  {#if $token && structure.canWrite}
    <LinkButton to={editLink} label="Éditer" small />
  {/if}
</div>
<div class="col-span-full lg:col-start-6 lg:col-end-13 lg:mt-s64">
  <p class="mb-s24 font-bold text-gray-dark">{structure.shortDesc}</p>
  <p class="prose">{@html structure.fullDesc}</p>
</div>

<style lang="postcss">
  .icon-label {
    @apply flex flex-row  items-baseline justify-start;
  }
  .icon-label a {
    @apply flex-initial;
  }

  .icon-label p {
    @apply flex-initial;
  }
  .icon {
    @apply relative top-s2 mr-s8 h-s16 w-s16 flex-none fill-current text-magenta-cta;
  }

  .ext-icon {
    @apply relative top-s2 ml-s8 h-s16 w-s16 flex-none fill-current;
  }
</style>
