<script lang="ts">
  import type { Snippet } from "svelte";

  import { Tooltip } from "bits-ui";

  interface Props {
    delayDuration?: number;
    side?: "top" | "bottom" | "left" | "right";
    children?: Snippet;
    content?: Snippet;
  }

  let {
    delayDuration = 0,
    side = "bottom",
    children,
    content,
  }: Props = $props();
</script>

<Tooltip.Provider>
  <Tooltip.Root {delayDuration}>
    <Tooltip.Trigger>
      {#if children}
        {@render children()}
      {/if}
    </Tooltip.Trigger>
    <Tooltip.Content
      class="text-gray-dark text-f12 py-s2 px-s8 rounded-sm bg-white leading-20 shadow-md"
      {side}
    >
      {#if content}
        {@render content()}
      {/if}
      <Tooltip.Arrow class="shadow-[-1px_-1px_2px_0_rgba(0,0,0,0.2)]" />
    </Tooltip.Content>
  </Tooltip.Root>
</Tooltip.Provider>
