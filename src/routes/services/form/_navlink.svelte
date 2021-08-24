<script>
  export let name;
  export let active;
  export let lit;
</script>

<style>
  button {
    padding: 0 var(--s16);
    border-bottom: 2px solid var(--col-gray-02);
    color: var(--col-text-alt2);
    font-size: var(--f16);
    text-align: center;
  }

  .active {
    border-bottom: 4px solid var(--col-magenta-brand);
    color: var(--col-magenta-cta);
  }
</style>

<button type="button" href="" on:click class:active disabled={!lit}>
  {name}
</button>
