<script lang="ts">
  import type { Component } from "svelte";

  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  interface Props {
    icon: Component;
    text: string;
    link?: string;
    isPreference?: boolean;
  }

  let { icon: Icon, text, link, isPreference = false }: Props = $props();
</script>

<li class="text-gray-text flex items-center">
  <span class="mr-s8 h-s24 w-s24 inline-block fill-current">
    <Icon />
  </span>

  {#if link}
    <a href={link} class="text-magenta-cta hover:underline" target="_blank">
      {text}
      <span class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current">
        <ExternalLinkLineSystem size="20" />
      </span>
    </a>
  {:else}
    {text}
  {/if}

  {#if isPreference}
    <span
      class="ml-s12 bg-magenta-20 px-s10 py-s6 text-f12 text-magenta-cta inline-block rounded-sm"
    >
      À privilégier
    </span>
  {/if}
</li>
