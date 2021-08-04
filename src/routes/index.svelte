<script context="module">
  import { getStructures } from "$lib/structures.js";

  export async function load({ _page, _fetch, _session, _context }) {
    return await getStructures();
  }
</script>

<script>
  import LinkButton from "$lib/components/link-button.svelte";
  export let structures;
</script>

<div class="flex flex-col items-start gap-3">
  <LinkButton label="Design System" to="design-system" />
  <LinkButton label="Création de structure" to="/structures/creer" />
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
