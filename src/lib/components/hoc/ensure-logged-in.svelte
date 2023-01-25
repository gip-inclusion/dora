<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { token, userInfo } from "$lib/utils/auth";
  import { onMount } from "svelte";

  onMount(() => {
    if (!$token) {
      const searchParams = $page.url.searchParams;
      const loginHint = searchParams.get("login_hint");
      if (loginHint) {
        searchParams.delete("login_hint");
        goto(
          `/auth/connexion?next=${encodeURIComponent(
            $page.url.pathname + $page.url.search
          )}&login_hint=${encodeURIComponent(loginHint)}`
        );
      } else {
        goto(
          `/auth/connexion?next=${encodeURIComponent(
            $page.url.pathname + $page.url.search
          )}`
        );
      }
    }
  });
</script>

{#if $userInfo}
  <slot />
{/if}
