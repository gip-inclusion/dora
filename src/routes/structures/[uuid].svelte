<script context="module">
  import { API_URL } from "../env.js";

  export async function load({ page, fetch, _session, _context }) {
    const url = `${API_URL}/structures/${page.params.uuid}/`;
    const res = await fetch(url);

    if (res.ok) {
      return {
        props: {
          structure: await res.json(),
        },
      };
    }
    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  }
</script>

<script>
  export let structure;
</script>

<svelte:head>
  <title>Dora: {structure.name}</title>
</svelte:head>

{structure.name}
