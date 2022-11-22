<script lang="ts">
  export let noPadding = false;
  export let extraClass = "";
  export let bgColor = "bg-white";
</script>

<div class="{extraClass} wrapper {bgColor} print:bg-white">
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
