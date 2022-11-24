<script lang="ts">
  import { onMount } from "svelte";

  function generateError() {
    // @ts-expect-error: function inexistante pour tester Sentry
    // eslint-disable-next-line
    myUndefinedFunction();
  }
  onMount(() => {
    generateError();
  });
</script>
