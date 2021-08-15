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
    margin-left: auto;
    margin-right: auto;
    grid-template-columns: repeat(12, 78px);
    column-gap: var(--s24);
    row-gap: 1.5rem;
  }

  .sticky {
    position: sticky;
    width: 100%;
    padding: var(--s24);
    bottom: 10px;
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15), 0 0 3px 0 rgba(0, 0, 0, 0.1);
    background-color: var(--col-bg);
    z-index: 50;
    will-change: transform;
  }

  .roundedbg {
    border-top-left-radius: 2.5rem /* 40px */;
    border-top-right-radius: 2.5rem /* 40px */;
    background-color: var(--col-gray-bg);
  }

  .bordertop {
    border-top-width: 1px;
    border-color: var(--col-gray3);
  }
</style>

<div
  class="wrapper"
  style="grid-row-start: {gridRow}"
  class:sticky
  class:roundedbg
  class:bordertop>
  <div class="centered">
    <slot />
  </div>
</div>
