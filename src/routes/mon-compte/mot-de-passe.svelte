<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import PasswordForm from "./_form-password.svelte";
</script>

<svelte:head>
  <title>Mon compte | Mot de passe | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <PasswordForm />
</EnsureLoggedIn>
