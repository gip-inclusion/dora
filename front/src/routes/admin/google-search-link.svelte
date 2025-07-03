<script lang="ts">
  import SmallLink from "./small-link.svelte";

  let { searchString } = $props();
</script>

<SmallLink
  link="https://www.google.com/search?&q={encodeURIComponent(searchString)}"
  label="google"
/>
