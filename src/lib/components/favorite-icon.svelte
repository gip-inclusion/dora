<script lang="ts">
  import { userInfo } from "$lib/auth";
  import { starSmileFillIcon, starSmileLineIcon } from "$lib/icons";

  export let active = false;
  export let inverted = false;
  export let big = false;
  export let small = false;

  $: currentIcon = active ? starSmileFillIcon : starSmileLineIcon;
</script>

{#if $userInfo}
  <button
    class="icon inline-block h-s24 w-s24 shrink-0 fill-current text-gray-text-alt2 hover:text-magenta-cta print:hidden"
    class:active
    class:inverted
    class:big
    class:small
    aria-label={active ? "Supprimer des favoris" : "Ajouter aux favoris"}
    on:click
  >
    {@html currentIcon}
  </button>
{/if}

<style lang="postcss">
  .active {
    @apply text-magenta-cta;
  }

  .inverted {
    @apply text-gray-01 hover:text-white;
  }

  .inverted.active {
    @apply text-white;
  }

  .big {
    @apply h-s24 w-s24 md:h-s32 md:w-s32;
  }

  .small {
    @apply h-s20 w-s20;
  }
</style>
