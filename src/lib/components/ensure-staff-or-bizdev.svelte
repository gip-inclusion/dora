<script>
  import { onMount } from "svelte";
  import { userInfo } from "$lib/auth";

  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import { token } from "$lib/auth";

  onMount(() => {
    if (!$token) {
      goto(`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`);
    }
  });
</script>

{#if $userInfo?.isStaff || $userInfo?.isBizdev}
  <slot />
{/if}
