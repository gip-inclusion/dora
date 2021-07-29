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

<h1 class="my-20 text-2xl font-extrabold">Liste des structures&nbsp;:</h1>

<div class="flex-col space-y-2">
  {#each structures as structure}
    <div
      class="px-6 py-2 text-xl text-dora-magenta-brand hover:text-dora-magenta-hover">
      <a href="/structures/{structure.id}">{structure.name}</a>
    </div>
  {/each}
</div>
