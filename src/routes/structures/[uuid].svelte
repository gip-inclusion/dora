<script context="module">
  import { getApiURL } from "$lib/utils";

  export async function load({ page, fetch, _session, _context }) {
    const url = `${getApiURL()}/structures/${page.params.uuid}/`;
    const res = await fetch(url, {
      headers: {
        Accept: "application/json; version=1.0",
      },
    });

    if (res.ok) {
      const structure = await res.json();
      return {
        props: {
          structure,
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
  import insane from "insane";

  import { markdownToHTML } from "$lib/utils";
  export let structure;

  function format_text(text) {
    return insane(
      markdownToHTML(
        text
          .replace(/ ;/gi, "&nbsp;;")
          .replace(/ :/gi, "&nbsp;:")
          .replace(/ !/gi, "&nbsp;!")
          .replace(/ \?/gi, "&nbsp;?")
      )
    );
  }
</script>

<svelte:head>
  <title>Dora: {structure.name}</title>
</svelte:head>

<h1 class="text-2xl mt-20 mb-4 font-bold">{structure.name}</h1>

<div class="flex-col space-y-4 text-sm text-gray-600">
  <div class="">
    <span class="">{structure.address}</span><br />
    <span class="">{structure.postalCode}</span>
    <span class="">{structure.city}</span>
  </div>

  <div class="prose prose-xl">
    {@html format_text(structure.shortDesc)}
  </div>

  <div class="prose max-w-3xl bg-gray-200 p-5">
    {@html format_text(structure.fullDesc)}
  </div>

  <div class="text-blue-dora font-bold">
    <a class="my-20" href={structure.url}>{structure.url}</a>
  </div>
  <div class="flex-row space-x-2">
    {#each structure.solutionsThemes as theme}
      <span class="rounded-xl bg-orange-400 p-0.5 px-4 text-white">
        {theme}</span>
    {/each}
  </div>
</div>
