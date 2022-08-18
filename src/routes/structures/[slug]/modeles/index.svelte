<script context="module">
  import { browser } from "$app/env";
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";
  import { structure } from "../_store";

  export async function load() {
    // sur le serveur, info est toujours null,
    // on retourne une 404 uniquement sur le client
    if (!browser) {
      return {};
    }

    const info = get(userInfo);
    const struct = get(structure);

    const isMember = struct.isMember || info?.isBizdev || info?.isStaff;

    if (!info || !struct || !isMember) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    return {};
  }
</script>

<script>
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import { capitalize } from "$lib/utils.js";

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
