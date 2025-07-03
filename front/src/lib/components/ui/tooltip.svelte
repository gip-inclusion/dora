<script lang="ts">
  import { Tooltip } from "bits-ui";

  interface Props {
    openDelay?: number;
    closeDelay?: number | undefined;
    side?: "top" | "bottom" | "left" | "right";
    children?: import('svelte').Snippet;
    content?: import('svelte').Snippet;
  }

  let {
    openDelay = 0,
    closeDelay = undefined,
    side = "bottom",
    children,
    content
  }: Props = $props();
</script>

<Tooltip.Root {openDelay} {closeDelay}>
  <Tooltip.Trigger>
    {@render children?.()}
  </Tooltip.Trigger>
  <Tooltip.Content
    class="text-gray-dark text-f12 py-s2 px-s8 rounded-sm bg-white leading-20 shadow-md"
    {side}
  >
    {@render content?.()}
    <Tooltip.Arrow class="shadow-[-1px_-1px_2px_0_rgba(0,0,0,0.2)]" />
  </Tooltip.Content>
</Tooltip.Root>
