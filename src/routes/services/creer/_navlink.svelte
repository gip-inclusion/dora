<script>
  import { page } from "$app/stores";

  export let target;
  export let name;

  $: isActive = $page.path.endsWith(target);
</script>

<a
  href={target}
  class={"text-center text-xs px-2 " +
    (isActive ? "border-blue-dora border-b-4" : "border-gray-300 border-b-2")}>
  {name}
</a>
