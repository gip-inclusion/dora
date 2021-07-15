<script context="module">
  export const load = async ({ page }) => ({
    props: {
      next: page.query.get("next"),
    },
  });
</script>

<script>
  import { goto } from "$app/navigation";
  import { clearToken } from "$lib/auth";

  export let next;

  clearToken();
  localStorage.clear();
  goto(next || "/");
</script>
