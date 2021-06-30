<script>
  import { onMount } from "svelte";
  import { API_URL } from "./env.js";
  let structures = [];

  onMount(async () => {
    const res = await fetch(`${API_URL}/structures/`, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });
    const jsonResult = await res.json();
    structures = jsonResult;
    console.log(structures);
  });
</script>

<h1 class="text-2xl font-extrabold my-20">Liste des structures&nbsp;:</h1>

<div class="flex-col space-y-2">
  {#each structures as structure}
    <div class="text-xl text-blue-dora py-2 px-6">
      <a href="/structures/{structure.id}">{structure.name}</a>
    </div>
  {/each}
</div>
