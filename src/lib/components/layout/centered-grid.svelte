<script>
  export let sticky = false;
  export let topPadded = false;
  export let roundedbg = false;
  export let bordertop = false;
  export let extraClass = "";
</script>

<div class="{extraClass} wrapper" class:sticky>
  <div
    class="flex justify-center px-s16 md:px-s40"
    class:roundedbg
    class:bordertop
  >
    <div
      class="centered-grid mx-auto grid gap-s24"
      class:top-padded={topPadded}
    >
      <slot />
    </div>
  </div>
</div>

<style lang="postcss">
  /* Color under the rounded corners */
  .wrapper {
    background-color: var(--col-under-bg, var(--col-bg));
  }

  .centered-grid {
    grid-template-columns: repeat(12, minmax(1px, 78px));
  }

  .sticky {
    position: sticky;
    z-index: 50;
    bottom: 0;
    width: 100%;
    padding: var(--s24);
    background-color: var(--col-bg);
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15), 0 0 3px 0 rgba(0, 0, 0, 0.1);
    will-change: transform;
  }

  .roundedbg {
    background-color: var(--col-content-bg, var(--col-gray-bg));
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

    .roundedbg {
      background-color: var(--col-white) !important;
    }
  }

  @screen lg {
    .roundedbg {
      background-color: var(--col-content-bg, var(--col-gray-bg));
      border-top-left-radius: var(--s40);
      border-top-right-radius: var(--s40);
    }
  }
</style>
