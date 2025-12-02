<script lang="ts">
  import type { Snippet } from "svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import { getToken, userInfo } from "$lib/utils/auth";
  import { onMount } from "svelte";
  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();

  onMount(() => {
    if (!getToken()) {
      const searchParams = page.url.searchParams;
      const loginHint = searchParams.get("login_hint");
      if (loginHint) {
        searchParams.delete("login_hint");
        goto(
          `/auth/connexion?next=${encodeURIComponent(
            page.url.pathname + page.url.search
          )}&login_hint=${encodeURIComponent(loginHint)}`
        );
      } else {
        goto(
          `/auth/connexion?next=${encodeURIComponent(
            page.url.pathname + page.url.search
          )}`
        );
      }
    }
  });
</script>

{#if $userInfo}
  {@render children?.()}
{/if}
