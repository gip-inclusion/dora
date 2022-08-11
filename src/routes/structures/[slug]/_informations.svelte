<script>
  import { token, userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import Notice from "$lib/components/notice.svelte";
  import TextClamp from "$lib/components/text-clamp.svelte";
  import {
    computerIcon,
    externalLinkIcon,
    mailIcon,
    mapPinIcon,
    phoneIcon,
  } from "$lib/icons";
  import { isStructureInformationsComplete } from "$lib/structures";
  import { markdownToHTML } from "$lib/utils";

  export let structure;

  let fullDesc;

  $: fullDesc = markdownToHTML(structure.fullDesc);
</script>

<div class="flex-common-css flex-col-reverse md:flex-row">
  <div class="flex-[1]">
    <div class="flex flex-col md:flex-row">
      <div class="mb-s24 md:mb-s0">
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

        {#if structure.phone}
          <p class="icon-label text-f14">
            <i class="icon mr-s8 text-magenta-cta">
              {@html phoneIcon}
            </i>
            <a href="tel:{structure.phone}">
              {structure.phone}
            </a>
          </p>
        {/if}
      </div>
    </div>
  </div>

  <div class="flex-[3]">
    {#if $token && (structure.isAdmin || $userInfo?.isStaff)}
      {#if !isStructureInformationsComplete(structure)}
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
      {:else}
        <div class="text-right">
          <LinkButton
            to={`/structures/${structure.slug}/editer`}
            label="Modifier"
            small
          />
        </div>
      {/if}
    {/if}
  </div>
</div>

<div class="flex-common-css">
  <div class="hidden flex-[1] md:block" />
  <div class="mb-s24 flex-[3] md:mt-s24">
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

  .flex-common-css {
    @apply flex gap-s40 md:gap-s40 lg:gap-s96;
  }
</style>
