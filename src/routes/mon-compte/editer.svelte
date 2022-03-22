<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import InformationsForm from "./_form-informations.svelte";
</script>

<svelte:head>
  <title>Mon compte | Éditer | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <div class="col-span-8 col-start-1 mb-s32">
    <InformationsForm modify formTitle="Informations" visible />
  </div>
</EnsureLoggedIn>
