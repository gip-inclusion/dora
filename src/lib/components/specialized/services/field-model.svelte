<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Tag from "$lib/components/display/tag.svelte";
  import {
    arraysCompare,
    markdownToHTML,
    htmlToMarkdown,
  } from "$lib/utils/misc";

  export let value: any | undefined = undefined;
  export let onUseValue: (() => void) | undefined = undefined;
  export let showUseButton = true;
  export let showModel = false;
  export let type = "text";
  export let options: any | undefined = undefined;

  export let paddingTop = false;
  export let serviceValue: any | undefined = undefined;

  let haveSameValue = false;

  function compare(val1, val2) {
    if (type === "array" || type === "files") {
      return arraysCompare(val1, val2);
    }

    // tiptap insère des caractères en fin de chaine.
    // on les supprime pour faire la comparaison
    if (type === "markdown") {
      // la description du service est passée par l'éditeur, ce qui réécrit les liens.
      // on le simule ainsi:
      const rewrittenVal1 = htmlToMarkdown(markdownToHTML(val1));
      return rewrittenVal1.trim() === val2.trim();
    }

    return val1 === val2;
  }

  function handleUseValue(_evt: MouseEvent) {
    onUseValue && onUseValue();
  }

  $: haveSameValue = showModel && compare(value, serviceValue);
</script>

<div
  class:flex={showModel}
  class:flex-col={showModel}
  class:lg:flex-row={showModel}
  class:lg:gap-s32={showModel}
  class:gap-s16={showModel}
>
  <div class={showModel ? "lg:w-2/3" : ""}>
    <slot />
  </div>
  {#if showModel}
    <div
      class="flex flex-col-reverse gap-s12 lg:w-1/3 lg:flex-col"
      class:lg:pt-s40={paddingTop}
      class:lg:gap-s0={haveSameValue}
    >
      {#if haveSameValue}
        <small class="lg:pt-s8">Pas de différence</small>
      {:else}
        <div class="rounded bg-info-light px-s12 py-s8">
          {#if value === "" || value === undefined || value === null || (Array.isArray(value) && !value.length)}
            <small class="mb-s8 lg:pt-s8">Champs vide</small>
          {:else if type === "array"}
            <div class="flex flex-wrap gap-s8">
              {#each value as v}
                <Tag
                  >{options.find((option) => option.value === v)?.label ||
                    v}</Tag
                >
              {/each}
            </div>
          {:else if type === "files"}
            <div class="flex flex-wrap gap-s8">
              {#each value as v}
                <Tag>{v}</Tag>
              {/each}
            </div>
          {:else if type === "markdown"}
            {@html markdownToHTML(value, 2)}
          {:else if type === "boolean"}
            <p class="mb-s0 text-f14">{value === true ? "Oui" : "Non"}</p>
          {:else if type === "text"}
            <p class="mb-s0 text-f14 text-gray-text">{value}</p>
          {/if}
        </div>
      {/if}

      <div class="flex items-center">
        <h5 class="mb-s0 lg:hidden">Modèle</h5>
        {#if !haveSameValue && showUseButton}
          <div class="ml-auto lg:ml-s0">
            <Button
              label="Utiliser"
              small
              secondary
              on:click={handleUseValue}
            />
          </div>
        {/if}
      </div>
    </div>

    <hr class="-mx-s32 mt-s12 lg:hidden" />
  {/if}
</div>
