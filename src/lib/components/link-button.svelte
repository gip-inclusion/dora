<script>
  import { goto } from "$app/navigation";

  import Button from "./button.svelte";

  export let to;
  export let small;

  function handleClick() {
    if (to) {
      goto(to);
    }
  }
</script>

<Button type="button" {...$$restProps} on:click={handleClick} {small} />
