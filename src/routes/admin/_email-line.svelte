<script>
  import CopyableText from "./_copyable-text.svelte";

  import SmallLink from "./_small-link.svelte";
  import WebSearchLink from "./_web-search-link.svelte";

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
