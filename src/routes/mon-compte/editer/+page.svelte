<script lang="ts">
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import InformationsForm from "../form-informations.svelte";
</script>

<EnsureLoggedIn>
  <InformationsForm modify formTitle="Informations" />
</EnsureLoggedIn>
