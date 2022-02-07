<script>
  import { onMount } from "svelte";

  function generateError() {
    // eslint-disable-next-line
    myUndefinedFunction();
  }
  onMount(() => {
    generateError();
  });
</script>
