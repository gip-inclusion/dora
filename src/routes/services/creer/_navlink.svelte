<script>
  import { page } from "$app/stores";

  export let target;
  export let name;

  $: active = $page.path.endsWith(target);
</script>

<style>
  a {
    padding: 0 var(--s16);
    border-bottom: 2px solid var(--col-gray-02);
    color: var(--col-text-alt2);
    cursor: default;
    font-size: var(--f16);
    text-align: center;
  }

  .active {
    border-bottom: 4px solid var(--col-magenta-brand);
    color: var(--col-magenta-cta);
  }
</style>

<a href="" class:active>
  {name}
</a>
