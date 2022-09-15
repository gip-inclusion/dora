<script>
  import { onMount } from "svelte";
  import { token, userInfo } from "$lib/auth";

  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  onMount(() => {
    if (!$token) {
      let searchParams = $page.url.searchParams;
      const loginHint = searchParams.get("login_hint");
      if (loginHint) {
        searchParams.delete("login_hint");
      }
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}&login_hint=${encodeURIComponent(loginHint)}`
      );
    }
  });
</script>

{#if $userInfo}
  <slot />
{/if}
