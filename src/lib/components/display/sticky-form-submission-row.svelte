<script lang="ts">
  import CenteredGrid from "./centered-grid.svelte";
</script>

<div class="sticky bottom-s0 z-10 border-t border-t-gray-02 shadow-md">
  <CenteredGrid noPadding>
    <div class="flex flex-row justify-end gap-s12 py-s24">
      <slot />
    </div>
  </CenteredGrid>
</div>
