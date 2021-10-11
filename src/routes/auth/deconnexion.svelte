<script>
  import { browser } from "$app/env";
  import { disconnect } from "$lib/auth";

  if (browser) {
    disconnect();
    // Forces a browser reload
    window.location = "/";
  }
</script>
