<script lang="ts">
  export let noPadding = false;
  export let extraClass = "";
  export let bgColor = "bg-white";
  export let roundedColor = "";
</script>

<div class={roundedColor} class:bg-white={roundedColor}>
  <div
    class="{extraClass} {bgColor} {roundedColor
      ? 'md:rounded-t-[30px] lg:rounded-t-[45px] xl:rounded-t-[60px]'
      : ''}"
  >
    <div class="px-s16 md:px-s40">
      <div
        class="mx-auto max-w-6xl"
        class:pt-s40={!noPadding}
        class:pb-s40={!noPadding}
      >
        <slot />
      </div>
    </div>
  </div>
</div>
