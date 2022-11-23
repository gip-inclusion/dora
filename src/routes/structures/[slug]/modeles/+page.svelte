<script lang="ts">
  import { structure } from "../_store";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import { capitalize } from "$lib/utils";

  import List from "./_list.svelte";
</script>

<svelte:head>
  <title>Modèles | {capitalize($structure.name)} | DORA</title>
  <meta name="description" content={$structure.shortDesc} />
</svelte:head>

<EnsureLoggedIn>
  <List
    models={$structure.models || []}
    structure={$structure}
    total={$structure.models.length}
  />
</EnsureLoggedIn>
