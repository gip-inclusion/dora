<script>
  export let noPadding = false;
  export let bordertop = false;
  export let extraClass = "";
</script>

<div class="{extraClass} wrapper">
  <div class="px-s16 md:px-s40" class:bordertop>
    <div
      class="mx-auto max-w-6xl"
      class:top-padded={!noPadding}
      class:pb-s40={!noPadding}
    >
      <slot />
    </div>
  </div>
</div>

<style lang="postcss">
  /* Color under the rounded corners */
  .wrapper {
    background-color: var(--col-bg);
  }

  .bordertop {
    border-color: var(--col-gray-03);
    border-top-width: 1px;
  }

  .top-padded {
    padding-top: var(--s40);
  }

  @media print {
    .top-padded {
      padding-top: 0;
    }

    .wrapper {
      background-color: var(--col-white) !important;
    }

    .content {
      background-color: var(--col-white) !important;
    }
  }
</style>
