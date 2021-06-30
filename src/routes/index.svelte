<script>
  import { onMount } from "svelte";
  import { API_URL } from "./env.js";
  let msg = null;

  onMount(async () => {
    const res = await fetch(`${API_URL}/hello/`, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });
    const jsonResult = await res.json();
    console.log(jsonResult);
    msg = jsonResult.message;
  });
</script>

<h1 class="text-6xl font-extrabold mb-20">Hello Dora !</h1>

<div>
  {#if msg}
    Le backend dit :
    <span class="text-xl bg-gray-600 text-white py-2 px-6 rounded shadow">
      {msg}
    </span>
  {:else}
    <span class="text-xl bg-gray-600 text-white py-2 px-6 rounded shadow">
      Le backend n'est pas connecté
    </span>
  {/if}
</div>
