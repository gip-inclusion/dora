<script>
  export let gridRow = 1;
  export let sticky = false;
  export let roundedbg = false;
  export let bordertop = false;
</script>

<style>
  .wrapper {
    display: flex;
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
    bottom: 10px;
    width: 100%;
    padding: var(--s24);
    background-color: var(--col-bg);
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15), 0 0 3px 0 rgba(0, 0, 0, 0.1);
    will-change: transform;
  }

  .roundedbg {
    background-color: var(--col-gray-bg);
    border-top-left-radius: 2.5rem /* 40px */;
    border-top-right-radius: 2.5rem /* 40px */;
  }

  .bordertop {
    border-color: var(--col-gray-03);
    border-top-width: 1px;
  }
</style>

<div
  class="wrapper"
  style="grid-row-start: {gridRow};"
  class:sticky
  class:roundedbg
  class:bordertop>
  <div class="centered">
    <slot />
  </div>
</div>
