<script>
  import { onMount } from "svelte";

  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import { token } from "$lib/auth";

  onMount(() => {
    if (!$token) {
      goto(`/auth/connexion?next=${encodeURIComponent($page.path)}`);
    }
  });
</script>

<slot />
