<script>
  import { token } from "$lib/stores";
  import { goto } from "$app/navigation";

  $token = null;
  localStorage.clear();
  goto("/");
</script>
