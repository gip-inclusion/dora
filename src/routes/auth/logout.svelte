<script context="module">
  export const load = async ({ page }) => ({
    props: {
      next: page.query.get("next"),
    },
  });
</script>

<script>
  import { goto } from "$app/navigation";
  import { browser } from "$app/env";
  import { clearToken } from "$lib/auth";

  export let next;

  if (browser) {
    clearToken();
    localStorage.clear();
    goto(next || "/");
  }
</script>
