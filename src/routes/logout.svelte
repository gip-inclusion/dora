<script>
  import { goto } from "$app/navigation";
  import { clearToken } from "$lib/auth";

  clearToken();
  localStorage.clear();
  goto("/");
</script>
