<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import { closeIcon, menuIcon } from "$lib/icons";

  let isOpen = false;

  afterNavigate(() => {
    isOpen = false;
  });
</script>

<div class="flex lg:hidden">
  <div>
    <button
      on:click={() => (isOpen = true)}
      class="text-gray-text"
      aria-expanded={isOpen}
      aria-controls="hamburger-content"
    >
      <span class="mt-s16 inline-block h-s24 w-s24 self-end text-gray-dark">
        {@html menuIcon}
      </span>
    </button>

    {#if isOpen}
      <div
        id="hamburger-content"
        class="fixed left-s0 right-s0 top-s0 z-20 h-[100%] overflow-y-auto bg-white p-s20"
      >
        <div class="flex justify-end">
          <button
            class="flex items-center pb-s20 text-magenta-cta"
            on:click={() => (isOpen = false)}
          >
            Fermer
            <span class="inline-block h-s24 w-s24 fill-current">
              {@html closeIcon}
            </span>
          </button>
        </div>

        <div>
          <slot />
        </div>
      </div>
    {/if}
  </div>
</div>

<div class="hidden lg:flex">
  <slot />
</div>
