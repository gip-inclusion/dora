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
      class="bottom-s8 right-s8 rounded-ml border-gray-02 p-s24 fixed z-10 w-[384px] border bg-white shadow-sm"
    >
      <div class="relative">
        <div class="right-s0 top-s0 absolute">
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
