<script lang="ts">
  interface Props {
    noPadding?: boolean;
    extraClass?: string;
    bgColor?: string;
    roundedColor?: string;
    children?: import('svelte').Snippet;
  }

  let {
    noPadding = false,
    extraClass = "",
    bgColor = "bg-white",
    roundedColor = "",
    children
  }: Props = $props();

  const padding = noPadding ? "" : "pt-s40 pb-s40";
</script>

<div class={roundedColor} class:bg-white={roundedColor}>
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
