<script lang="ts">
  import { externalLinkIcon } from "$lib/icons";

  export let icon: string;
  export let text: string;
  export let link: string | undefined = undefined;
  export let isPreference = false;
</script>

<li class="flex items-center text-gray-text">
  <span class="mr-s8 inline-block h-s24 w-s24 fill-current">
    {@html icon}
  </span>

  {#if link}
    <a href={link} class="text-magenta-cta hover:underline" target="_blank">
      {text}
      <span class="inline-block h-s20 w-s20 fill-current pl-s4 pt-s6">
        {@html externalLinkIcon}
      </span>
    </a>
  {:else}
    {text}
  {/if}

  {#if isPreference}
    <span
      class="ml-s12 inline-block rounded bg-magenta-20 px-s10 py-s6 text-f12 text-magenta-cta"
    >
      À privilégier
    </span>
  {/if}
</li>
