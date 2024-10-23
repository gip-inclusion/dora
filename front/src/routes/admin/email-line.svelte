<script lang="ts">
  import CopyableText from "./copyable-text.svelte";

  export let email;
</script>

{#if email}
  <div>
    ✉️ <a href="mailto:{email}">{email}</a>
    <CopyableText text={email} />
  </div>
{/if}
