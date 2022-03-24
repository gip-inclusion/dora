<script>
  import { token, userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import {
    computerIcon,
    externalLinkIcon,
    mailIcon,
    mapPinIcon,
    phoneIcon,
  } from "$lib/icons";

  export let structure;
</script>

<div class="col-span-full md:flex md:items-center md:justify-between">
  <h2 class="mb-s24 text-france-blue">Informations</h2>

  {#if $token && (structure.isAdmin || $userInfo?.isStaff)}
    <LinkButton
      to={`/structures/${structure.slug}/editer`}
      label="Modifier…"
      small
    />
  {/if}
</div>

<div class="col-span-full mb-s24 lg:col-start-1 lg:col-end-4">
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
      <a target="_blank" rel="noopener nofollow" href={structure.url}>
        {structure.url}
      </a>
      <i class="icon ml-s8">
        {@html externalLinkIcon}
      </i>
    </p>
  {/if}

  {#if structure.email}
    <p class="icon-label text-f14">
      <i class="icon mr-s8 text-magenta-cta">
        {@html mailIcon}
      </i>

      <a href="mailto:{structure.email}">
        {structure.email}
      </a>
      <i class="icon ml-s8">
        {@html externalLinkIcon}
      </i>
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

<div class="col-span-full lg:col-start-4 lg:col-end-11">
  <p class="mb-s24 font-bold text-gray-dark">{structure.shortDesc}</p>
  <p class="prose mb-s24">{@html structure.fullDesc}</p>
</div>

<style lang="postcss">
  .icon-label {
    @apply flex flex-row items-baseline justify-start;
  }

  .icon-label a {
    @apply flex-initial;
  }

  .icon-label p {
    @apply flex-initial;
  }

  .icon {
    @apply relative top-s2 h-s16 w-s16 flex-none fill-current;
  }
</style>
