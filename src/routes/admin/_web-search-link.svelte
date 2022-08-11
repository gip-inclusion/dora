<script>
  import SmallLink from "./_small-link.svelte";

  export let searchString;
</script>

<SmallLink
  link="https://www.google.com/search?&q={encodeURIComponent(searchString)}"
  label="google"
/>
