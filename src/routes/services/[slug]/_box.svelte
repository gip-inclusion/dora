<script>
  export let title = "";
</script>

<style>
  .wrapper {
    overflow: hidden;
    border: 1px solid var(--box-color);
    margin: 20px 0;
    border-radius: 4px;
  }

  .title {
    padding: 2px;
    background: var(--box-color);
    color: var(--col-white);
  }

  .content {
    padding: 6px;
  }
</style>

<div class="wrapper">
  <div class="title">
    <strong>{title}</strong>
  </div>
  <div class="content">
    <slot />
  </div>
</div>
