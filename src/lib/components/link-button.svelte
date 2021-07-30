<script>
  import { goto } from "$app/navigation";

  import Button from "./button.svelte";

  export let to;

  function handleClick() {
    if (to) {
      goto(to);
    }
  }
</script>

<Button {...$$restProps} on:click={handleClick} />
