<script lang="ts">
  import { externalLinkIcon } from "$lib/icons";

  interface Props {
    icon: string;
    text: string;
    link?: string;
    isPreference?: boolean;
  }

  let { icon, text, link, isPreference = false }: Props = $props();
</script>

<li class="text-gray-text flex items-center">
  <span class="mr-s8 h-s24 w-s24 inline-block fill-current">
    {@html icon}
  </span>

  {#if link}
    <a href={link} class="text-magenta-cta hover:underline" target="_blank">
      {text}
      <span class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current">
        {@html externalLinkIcon}
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
