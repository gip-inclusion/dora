<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import { closeIcon, menuIcon } from "$lib/icons";
  interface Props {
    children?: import("svelte").Snippet;
  }

  let { children }: Props = $props();

  let isOpen = $state(false);

  afterNavigate(() => {
    isOpen = false;
  });
</script>

<div class="flex lg:hidden">
  <div>
    <button
      onclick={() => (isOpen = true)}
      class="text-gray-text"
      aria-expanded={isOpen}
      aria-controls="hamburger-content"
    >
      <span class="mt-s16 h-s24 w-s24 text-gray-dark inline-block self-end">
        {@html menuIcon}
      </span>
    </button>

    {#if isOpen}
      <div
        id="hamburger-content"
        class="left-s0 right-s0 top-s0 p-s20 fixed z-20 h-[100%] overflow-y-auto bg-white"
      >
        <div class="flex justify-end">
          <button
            class="pb-s20 text-magenta-cta flex items-center"
            onclick={() => (isOpen = false)}
          >
            Fermer
            <span class="h-s24 w-s24 inline-block fill-current">
              {@html closeIcon}
            </span>
          </button>
        </div>

        <div>
          {@render children?.()}
        </div>
      </div>
    {/if}
  </div>
</div>

<div class="hidden lg:flex">
  {@render children?.()}
</div>
