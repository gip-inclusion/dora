<script lang="ts">
  import SmallLink from "./small-link.svelte";

  interface Props {
    searchString: string;
  }

  let { searchString }: Props = $props();
</script>

<SmallLink
  link="https://www.google.com/search?&q={encodeURIComponent(searchString)}"
  label="google"
/>
