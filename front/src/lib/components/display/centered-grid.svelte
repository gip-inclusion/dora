<script lang="ts">
  export let noPadding = false;
  export let extraClass = "";
  export let bgColor = "bg-white";
  export let roundedColor = "";

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
        <slot />
      </div>
    </div>
  </div>
</div>
