<script lang="ts">
  import CopyableText from "./copyable-text.svelte";
  import SmallLink from "./small-link.svelte";
  import WebSearchLink from "./web-search-link.svelte";

  export let email;
</script>

{#if email}
  <div>
    ✉️ {email}
    <SmallLink link="mailto:{email}" label="mailto" />
    <WebSearchLink searchString={email} />
    <CopyableText text={email} />
  </div>
{/if}
