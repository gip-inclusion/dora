<script>
  import { page } from "$app/stores";

  export let target;
  export let name;

  $: isActive = $page.path.endsWith(target);
</script>

<a
  href={target}
  class={"text-center text-xs px-2 " +
    (isActive
      ? "border-dora-magenta-brand border-b-4"
      : "border-gray-02 border-b-2")}>
  {name}
</a>
