<script lang="ts">
  import SmallLink from "./small-link.svelte";

  export let searchString;
  export let kind: "people" | "companies";
</script>

<SmallLink
  link="https://www.linkedin.com/search/results/{kind}/?keywords={encodeURIComponent(
    searchString
  )}"
  label="linkedin"
/>
