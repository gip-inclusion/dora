<script>
  import { onMount } from "svelte";
  let msg = [];

  onMount(async () => {
    const res = await fetch(`http://localhost:8000/hello/`);
    const jsonResult = await res.json();
    console.log(jsonResult);
    msg = jsonResult.message;
  });
</script>

<h1>Dora</h1>
<p>
  Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
</p>

<div>
  {#if msg}
    {msg}
  {:else}
    <!-- this block renders when photos.length === 0 -->
    <p>loading...</p>
  {/if}
</div>
