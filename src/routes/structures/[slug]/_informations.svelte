<script>
  import { token, userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import TextClamp from "$lib/components/text-clamp.svelte";
  import {
    computerIcon,
    externalLinkIcon,
    mailIcon,
    mapPinIcon,
    phoneIcon,
  } from "$lib/icons";
  import { markdownToHTML } from "$lib/utils";

  export let structure;

  let fullDesc;

  $: fullDesc = markdownToHTML(structure.fullDesc);
</script>

<div class="md:flex md:items-center md:justify-between">
  <h2 class="mb-s24 text-france-blue">Informations</h2>

  {#if $token && (structure.isAdmin || $userInfo?.isStaff)}
    <LinkButton
      to={`/structures/${structure.slug}/editer`}
      label="Modifier"
      small
    />
  {/if}
</div>

<div class="flex flex-col gap-s40 md:flex-row">
  <div class="mb-s24 md:w-1/3">
    <p class="icon-label text-f14">
      <i class="icon mr-s8 text-magenta-cta">
        {@html mapPinIcon}
      </i>
      {structure.address1}
      {#if structure.address2}
        <br />{structure.address2}
      {/if}
      <br />{structure.postalCode}
      {structure.city}
    </p>

    {#if structure.url}
      <p class="icon-label text-f14">
        <i class="icon mr-s8 text-magenta-cta">
          {@html computerIcon}
        </i>
        <a
          target="_blank"
          title="Ouverture dans une nouvelle fenêtre"
          rel="noopener nofollow"
          href={structure.url}
          class="flex"
        >
          {structure.url}

          <i class="ml-s8 mt-s2 h-s16 w-s16 fill-current">
            {@html externalLinkIcon}
          </i>
        </a>
      </p>
    {/if}

    {#if structure.email}
      <p class="icon-label text-f14">
        <i class="icon mr-s8 text-magenta-cta">
          {@html mailIcon}
        </i>

        <a href="mailto:{structure.email}" class="flex">
          {structure.email}
          <i class="ml-s8 mt-s2 h-s16 w-s16 fill-current">
            {@html externalLinkIcon}
          </i>
        </a>
      </p>
    {/if}

    <p class="icon-label text-f14">
      <i class="icon mr-s8 text-magenta-cta">
        {@html phoneIcon}
      </i>
      <a href="tel:{structure.phone}">
        {structure.phone}
      </a>
    </p>
  </div>

  <div class="mb-s24 md:w-2/3">
    <p class="mb-s24 font-bold">{structure.shortDesc}</p>
    {#if fullDesc}
      <TextClamp text={fullDesc} />
    {/if}
  </div>
</div>

<style lang="postcss">
  .icon-label {
    @apply flex flex-row items-baseline justify-start;
  }

  .icon-label a {
    @apply flex-initial;
  }

  .icon {
    @apply relative top-s2 h-s16 w-s16 flex-none fill-current;
  }
</style>
