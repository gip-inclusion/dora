<script lang="ts">
  import SmallLink from "./small-link.svelte";

  interface Props {
    searchString: any;
    kind: "people" | "companies";
  }

  let { searchString, kind }: Props = $props();
</script>

<SmallLink
  link="https://www.linkedin.com/search/results/{kind}/?keywords={encodeURIComponent(
    searchString
  )}"
  label="linkedin"
/>
