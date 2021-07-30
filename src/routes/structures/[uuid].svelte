<script context="module">
  import { getApiURL } from "$lib/utils";
  import Button from "$lib/components/button.svelte";

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

  import RichText from "$lib/components/rich-text/editor.svelte";
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

<h1 class="">{structure.name}</h1>
{#if currentToken}
  {#if !editMode}
    <Button type="submit" on:click={handleEdit} label="Éditer" />
  {:else}
    <div class="flex flex-row gap-2">
      <Button type="cancel" on:click={handleCancel} label="Annuler" secondary />
      <Button type="submit" on:click={handleSave} label="Enregistrer" />
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
    <RichText
      bind:htmlContent={currentFullDesc}
      initialContent={currentFullDesc}
      className="prose prose-sm h-20" />
  {:else}
    <div class="max-w-3xl p-5 prose bg-gray-200">
      {@html format_text(structure.fullDesc)}
    </div>
  {/if}

  <div class="font-bold text-dora-magenta-brand">
    <a class="my-20" href={structure.url}>{structure.url}</a>
  </div>
  <!-- <div class="flex-row space-x-2">
    {#each structure.solutionsThemes as theme}
      <span class="rounded-xl bg-orange-400 p-0.5 px-4 text-white">
        {theme}</span>
    {/each}
  </div> -->
</div>
