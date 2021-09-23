<script>
  // import { goto } from "$app/navigation";
  import { browser } from "$app/env";
  import { clearToken, clearUserInfo } from "$lib/auth";

  if (browser) {
    clearToken();
    clearUserInfo();
    localStorage.clear();
    // goto("/");
    // Forces a browser reload
    window.location = "/";
  }
</script>
