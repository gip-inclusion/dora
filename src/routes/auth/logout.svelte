<script>
  import { goto } from "$app/navigation";
  import { browser } from "$app/env";
  import { clearToken } from "$lib/auth";

  if (browser) {
    clearToken();
    localStorage.clear();
    goto("/");
  }
</script>
