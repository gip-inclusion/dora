<script lang="ts">
  import CopyableText from "./copyable-text.svelte";

  let { email } = $props();
</script>

{#if email}
  <div>
    ✉️ <a href="mailto:{email}">{email}</a>
    <CopyableText text={email} />
  </div>
{/if}
