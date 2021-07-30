<script context="module">
  import { getApiURL } from "$lib/utils.js";

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
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<div class="flex flex-col items-start gap-3">
  <LinkButton label="Design System" to="design-system" />
  <LinkButton label="Création de service" to="/services/creer" />
</div>
<h2>Liste des structures&nbsp;:</h2>

<div class="flex-col space-y-2">
  {#each structures as structure}
    <div
      class="px-6 py-2 text-xl text-dora-magenta-brand hover:text-dora-magenta-hover">
      <a href="/structures/{structure.id}">{structure.name}</a>
    </div>
  {/each}
</div>
