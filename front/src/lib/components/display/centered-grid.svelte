<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    noPadding?: boolean;
    extraClass?: string;
    bgColor?: string;
    roundedColor?: string;
    children?: Snippet;
  }

  let {
    noPadding = false,
    extraClass = "",
    bgColor = "bg-white",
    roundedColor = "",
    children,
  }: Props = $props();

  const padding = noPadding ? "" : "pt-s32 pb-s32";
</script>

<div class={roundedColor}>
  <div
    class="{padding} {extraClass} {bgColor} {roundedColor
      ? 'md:rounded-t-[30px] lg:rounded-t-[45px] xl:rounded-t-[60px]'
      : ''} print:pb-s0"
  >
    <div class="px-s16 md:px-s40">
      <div class="mx-auto max-w-6xl">
        {@render children?.()}
      </div>
    </div>
  </div>
</div>
