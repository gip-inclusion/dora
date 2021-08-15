<script>
  export let class1, class2;
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
</style>

<div class="wrapper {class1}">
  <div class="centered {class2}">
    <slot />
  </div>
</div>
