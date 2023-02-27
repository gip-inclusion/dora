<script lang="ts">
  import CopyableText from "./copyable-text.svelte";
  import SmallLink from "./small-link.svelte";

  export let email;
</script>

{#if email}
  <div>
    ✉️ {email}
    <SmallLink link="mailto:{email}" label="mailto" />
    <CopyableText text={email} />
  </div>
{/if}
