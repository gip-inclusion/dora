<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import InformationsForm from "./_form-informations.svelte";
</script>

<svelte:head>
  <title>Mon compte | Éditer | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <InformationsForm modify formTitle="Informations" />
</EnsureLoggedIn>
