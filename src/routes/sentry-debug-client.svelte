<script context="module">
  export const ssr = false;
</script>

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
