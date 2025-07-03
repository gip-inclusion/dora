<script lang="ts">
  import CenteredGrid from "../display/centered-grid.svelte";

  interface Props {
    justifyBetween?: boolean;
    children?: import('svelte').Snippet;
  }

  let { justifyBetween = false, children }: Props = $props();
</script>

<div class="bottom-s0 sticky z-20">
  <div class="top-shadow bottom-s0 h-s24 sticky -z-10 bg-white"></div>
  <CenteredGrid noPadding>
    <div
      class="gap-s12 pb-s24 z-50 flex flex-row bg-white"
      class:justify-end={!justifyBetween}
      class:justify-between={justifyBetween}
    >
      {@render children?.()}
    </div>
  </CenteredGrid>
</div>

<style lang="postcss">
  @reference "../../../app.css";

  .top-shadow {
    box-shadow:
      0px 0px 2px rgba(0, 0, 0, 0.2),
      0px 2px 12px rgba(0, 0, 0, 0.1);
  }
</style>
