<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { token, userInfo } from "$lib/utils/auth";
  import { onMount } from "svelte";

  onMount(() => {
    if (!$token) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
    }
  });
</script>

{#if $userInfo?.isStaff || $userInfo?.isBizdev}
  <slot />
{/if}
