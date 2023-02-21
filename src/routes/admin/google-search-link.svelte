<script lang="ts">
  import SmallLink from "./small-link.svelte";

  export let searchString;
</script>

<SmallLink
  link="https://www.google.com/search?&q={encodeURIComponent(searchString)}"
  label="google"
/>
