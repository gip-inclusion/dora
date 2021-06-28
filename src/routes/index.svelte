<script>
  import { onMount } from "svelte";
  import { API_URL, THIS_SHOULD_NOT_WORK } from "./env.js";
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
  <pre>
    App Mode {import.meta.env.MODE}
    Base URL {import.meta.env.BASE_URL}
    PROD {import.meta.env.PROD}
    DEV {import.meta.env.DEV}
    API_URL {API_URL}
    DJANGO_ALLOWED_HOSTS {THIS_SHOULD_NOT_WORK}

  </pre>
</div>
