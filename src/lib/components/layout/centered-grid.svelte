<script>
  export let gridRow = 1;
  export let sticky = false;
  export let roundedbg = false;
  export let bordertop = false;
</script>

<style>
  .content {
    display: flex;
    background-color: var(--col-bg);
  }

  .centered {
    display: grid;
    margin-right: auto;
    margin-left: auto;
    column-gap: var(--s24);
    grid-template-columns: repeat(12, 78px);
    row-gap: 1.5rem;
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
    border-top-left-radius: var(--s40);
    border-top-right-radius: var(--s40);
  }

  .bordertop {
    border-color: var(--col-gray-03);
    border-top-width: 1px;
  }

  :global(.global-content-wrapper) .padded {
    padding-top: var(--s56);
    background-color: var(--col-bg);
  }

  /* Color under the rounded corners */
  .wrapper {
    background-color: var(--col-under-bg, var(--col-bg));
  }
</style>

<div class="wrapper" class:padded={gridRow === 1}>
  <div
    class="content"
    style="grid-row-start: {gridRow};"
    class:sticky
    class:roundedbg
    class:bordertop>
    <div class="centered">
      <slot />
    </div>
  </div>
</div>
