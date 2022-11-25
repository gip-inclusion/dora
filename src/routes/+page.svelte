<script lang="ts">
  import type { PageData } from "./$types";
  import Landing from "./homepage/landing.svelte";

  export let data: PageData;
</script>

<svelte:head>
  <title>DORA : recensement et mise à jour de l’offre d’insertion</title>
  <meta
    name="description"
    content="Le service public numérique de recensement et mise à jour de l’offre d’insertion."
  />
</svelte:head>

<Landing servicesOptions={data.servicesOptions} />
