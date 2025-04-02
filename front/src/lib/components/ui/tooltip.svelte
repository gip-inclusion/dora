<script lang="ts">
  import { Tooltip } from "bits-ui";

  export let openDelay: number = 0;
  export let closeDelay: number | undefined = undefined;
  export let side: "top" | "bottom" | "left" | "right" = "bottom";
</script>

<Tooltip.Root {openDelay} {closeDelay}>
  <Tooltip.Trigger>
    <slot />
  </Tooltip.Trigger>
  <Tooltip.Content
    class="text-gray-dark text-f12 py-s2 px-s8 rounded-sm bg-white leading-20 shadow-md"
    {side}
  >
    <slot name="content" />
    <Tooltip.Arrow class="shadow-[-1px_-1px_2px_0_rgba(0,0,0,0.2)]" />
  </Tooltip.Content>
</Tooltip.Root>
