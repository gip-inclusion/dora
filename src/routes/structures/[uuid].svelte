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

  import Tiptap from "$lib/tiptap.svelte";
  import { token } from "$lib/auth";
  import { markdownToHTML, htmlToMarkdown } from "$lib/utils";

  export let structure;

  let currentToken = $token;
  let currentFullDesc = format_text(structure.fullDesc);
  let editMode = false;

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

  function handleEdit() {
    editMode = true;
    currentFullDesc = format_text(structure.fullDesc);
  }

  function handleSave() {
    editMode = false;
    let newFullDesk = htmlToMarkdown(currentFullDesc);
    updateStructure("fullDesc", newFullDesk);
  }

  function handleCancel() {
    editMode = false;
    currentFullDesc;
  }

  async function updateStructure(field, value) {
    const oldValue = structure[field].trim();
    const newValue = value.trim();
    console.log(oldValue, newValue);
    if (oldValue !== newValue) {
      structure[field] = newValue;
      const url = `${getApiURL()}/structures/${structure.id}/`;
      const res = await fetch(url, {
        method: "PATCH",
        headers: {
          Accept: "application/json; version=1.0",
          "Content-Type": "application/json",
          Authorization: `Token ${currentToken}`,
        },
        body: JSON.stringify({
          [field]: newValue,
        }),
      });

      if (res.ok) {
        const newStructure = await res.json();
        structure = newStructure;
      }
      return {
        status: res.status,
        error: new Error(`Could not load ${url}`),
      };
    }
  }
</script>

<svelte:head>
  <title>Dora: {structure.name}</title>
</svelte:head>

<h1 class="mt-20 mb-4 text-2xl font-bold">{structure.name}</h1>
{#if currentToken}
  {#if !editMode}
    <button
      type="submit"
      on:click|preventDefault={handleEdit}
      disabled={false}
      class="block px-2 py-1 text-white border-2 rounded bg-action disabled:bg-back2 hover:bg-blue-dora">
      Éditer
    </button>
  {:else}
    <div class="flex flex-row">
      <button
        type="cancel"
        on:click|preventDefault={handleCancel}
        disabled={false}
        class="block px-2 py-1 text-white bg-gray-400 border-2 rounded disabled:bg-back2 hover:bg-blue-dora">
        Cancel
      </button>
      <button
        type="submit"
        on:click|preventDefault={handleSave}
        disabled={false}
        class="block px-2 py-1 text-white border-2 rounded bg-action disabled:bg-back2 hover:bg-blue-dora">
        Save
      </button>
    </div>
  {/if}
{/if}
<div class="flex-col space-y-4 text-sm text-gray-600">
  <div class="">
    <span class="">{structure.address}</span><br />
    <span class="">{structure.postalCode}</span>
    <span class="">{structure.city}</span>
  </div>

  <div class="prose prose-xl">
    {@html format_text(structure.shortDesc)}
  </div>
  {#if editMode}
    <Tiptap
      bind:htmlContent={currentFullDesc}
      initialContent={currentFullDesc}
      className="prose prose-sm p-2 whitespace-pre-wrap w-full max-w-none h-64 border-2 overflow-auto focus:outline-none" />
  {:else}
    <div class="max-w-3xl p-5 prose bg-gray-200">
      {@html format_text(structure.fullDesc)}
    </div>
  {/if}

  <div class="font-bold text-blue-dora">
    <a class="my-20" href={structure.url}>{structure.url}</a>
  </div>
  <!-- <div class="flex-row space-x-2">
    {#each structure.solutionsThemes as theme}
      <span class="rounded-xl bg-orange-400 p-0.5 px-4 text-white">
        {theme}</span>
    {/each}
  </div> -->
</div>
