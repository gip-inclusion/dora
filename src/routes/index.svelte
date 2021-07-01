<script context="module">
  import { getApiURL } from "$lib/utils";

  let structures = [];

  export async function load({ _page, fetch, _session, _context }) {
    const url = `${getApiURL()}/structures/`;
    const res = await fetch(url, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });

    if (res.ok) {
      structures = await res.json();
      return {
        props: {
          structures,
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
</script>

<h1 class="text-2xl font-extrabold my-20">Liste des structures&nbsp;:</h1>

<div class="flex-col space-y-2">
  {#each structures as structure}
    <div class="text-xl text-blue-dora py-2 px-6">
      <a href="/structures/{structure.id}">{structure.name}</a>
    </div>
  {/each}
</div>
