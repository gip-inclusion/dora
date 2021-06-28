<script>
  import { onMount } from "svelte";
  let msg = null;

  const api_url = import.meta.env.VITE_API_URL || "http://localhost:8000";
  onMount(async () => {
    const res = await fetch(`${api_url}/hello/`);
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
    API_URL {import.meta.env.VITE_API_URL}
    DJANGO_ALLOWED_HOSTS {import.meta.env.DJANGO_ALLOWED_HOSTS}

  </pre>
</div>
