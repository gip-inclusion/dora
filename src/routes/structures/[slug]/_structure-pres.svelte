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
    @apply w-2 h-2 mr-1 fill-current text-dora-magenta-cta relative top-2p flex-none;
  }

  .ext-icon {
    @apply w-2 h-2 ml-1 fill-current relative top-2p flex-none;
  }
</style>

<div class="col-span-full lg:col-start-1 lg:col-end-5 flex flex-col gap-2">
  <div
    class=" mt-8 text-gray-text text-sm flex flex-row flex-wrap gap-x-3 lg:gap-1 lg:flex-col"
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
<div class="col-span-full lg:col-start-6 lg:col-end-13 lg:mt-8">
  <p class="text-xl text-gray-dark font-bold mb-3">{structure.shortDesc}</p>
  <p class="prose">{@html structure.fullDesc}</p>
</div>
