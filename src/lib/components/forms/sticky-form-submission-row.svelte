<script lang="ts">
  import CenteredGrid from "../display/centered-grid.svelte";

  export let justifyBetween = false;
</script>

<div class="sticky bottom-s0 z-20">
  <div class="top-shadow sticky bottom-s0 -z-10 h-s24 bg-white" />
  <CenteredGrid noPadding>
    <div
      class="z-50 flex flex-row  gap-s12 bg-white pb-s24"
      class:justify-end={!justifyBetween}
      class:justify-between={justifyBetween}
    >
      <slot />
    </div>
  </CenteredGrid>
</div>

<style lang="postcss">
  .top-shadow {
    box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.2), 0px 2px 12px rgba(0, 0, 0, 0.1);
  }
</style>
