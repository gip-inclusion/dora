<script lang="ts">
  import Portal from "svelte-portal";

  import Button from "$lib/components/display/button.svelte";
  import { closeLineIcon } from "$lib/icons";

  export let isOpen: boolean;

  function handleClose() {
    isOpen = false;
  }
</script>

{#if isOpen}
  <Portal target={document.body}>
    <div
      class="fixed bottom-s8 right-s8 z-10 w-[384px] rounded-ml border border-gray-02 bg-white p-s24 shadow-sm"
    >
      <div class="relative">
        <div class="absolute right-s0 top-s0">
          <Button
            icon={closeLineIcon}
            on:click={handleClose}
            noBackground
            noPadding
          />
        </div>

        <slot />
      </div>
    </div>
  </Portal>
{/if}
