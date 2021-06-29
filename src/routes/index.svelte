<script>
  import { onMount } from "svelte";
  import { API_URL } from "./env.js";
  let msg = null;

  onMount(async () => {
    const res = await fetch(`${API_URL}/hello/`);
    const jsonResult = await res.json();
    console.log(jsonResult);
    msg = jsonResult.message;
  });
</script>

<h1>Hello Dora !</h1>

<div>
  {#if msg}
    Le backend dit : <span
      style="background-color: grey; color: white; padding: 0.2em;">{msg}</span
    >
  {:else}
    <p>Le backend n'est pas connecté</p>
  {/if}
</div>
