<script lang="ts">
  import Landing from "./_homepage/_landing.svelte";
  import type { PageData } from "./$types";

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
