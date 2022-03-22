<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import PasswordForm from "./_form-password.svelte";
</script>

<svelte:head>
  <title>Mon compte | Mot de passe | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <div class="col-span-8 col-start-1 mb-s32">
    <PasswordForm />
  </div>
</EnsureLoggedIn>
