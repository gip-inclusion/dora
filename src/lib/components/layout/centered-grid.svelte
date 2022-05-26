<script>
  export let noPadding = false;
  export let roundedTop = false;
  export let roundedBottom = false;
  export let bordertop = false;
  export let extraClass = "";
</script>

<div class="{extraClass} wrapper" class:roundedBottom>
  <div class="px-s16 md:px-s40" class:roundedTop class:bordertop>
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
    background-color: var(--col-under-bg, var(--col-bg));
  }

  .bordertop {
    border-color: var(--col-gray-03);
    border-top-width: 1px;
  }

  .top-padded {
    padding-top: var(--s40);
  }

  .roundedTop {
    background-color: var(--col-content-bg, var(--col-gray-bg));
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

    .roundedTop,
    .roundedBottom {
      background-color: var(--col-white) !important;
    }
  }

  @screen lg {
    .roundedBottom {
      background-color: var(--col-bg, var(--col-gray-bg));
    }

    .roundedTop {
      border-top-left-radius: var(--s40);
      border-top-right-radius: var(--s40);
    }

    .roundedBottom {
      border-bottom-left-radius: var(--s40);
      border-bottom-right-radius: var(--s40);
    }
  }
</style>
