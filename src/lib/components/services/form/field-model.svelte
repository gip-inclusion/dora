<script>
  import Button from "$lib/components/button.svelte";
  import Tag from "$lib/components/tag.svelte";

  export let value;
  export let useValue;
  export let showModel = false;
  export let type = "text";
  export let options = undefined;

  export let paddingTop = false;
  let hasValue;

  $: hasValue = value !== null && value !== undefined;
</script>

<div
  class:flex={showModel}
  class:flex-col={showModel}
  class:lg:flex-row={showModel}
  class:lg:gap-s32={showModel}
  class:gap-s16={showModel}
>
  <div class="{showModel ? 'lg:w-2/3' : ''} class">
    <slot />
  </div>
  {#if showModel}
    <div
      class="flex flex-col-reverse gap-s8 lg:w-1/3 lg:flex-col"
      class:lg:pt-s40={paddingTop}
      class:lg:gap-s0={!hasValue}
    >
      {#if !hasValue}
        <small class="lg:pt-s8">Pas de différence</small>
      {:else}
        <div class="rounded bg-info-light py-s8 px-s12">
          {#if value === "" || (Array.isArray(value) && !value.length)}
            <small class="mb-s8 lg:pt-s8">Champs vide</small>
          {:else if type === "list"}
            <div class="flex flex-wrap gap-s8">
              {#each value as v}
                <Tag>{options.find((o) => o.value === v)?.label || v}</Tag>
              {/each}
            </div>
          {:else if type === "html"}
            {@html value}
          {:else if type === "boolean"}
            <p class="mb-s0 text-f14">{value === true ? "Oui" : "Non"}</p>
          {:else if type === "text"}
            <p class="mb-s0 text-f14 text-gray-text">{value}</p>
          {/if}
        </div>
      {/if}

      <div class="flex items-center">
        <h5 class="mb-s0 lg:hidden">Modèle</h5>
        {#if hasValue}
          <div class="ml-auto lg:ml-s0">
            <Button label="Utiliser" small secondary on:click={useValue} />
          </div>
        {/if}
      </div>
    </div>

    <hr class="-mx-s32 mt-s12 lg:hidden" />
  {/if}
</div>
