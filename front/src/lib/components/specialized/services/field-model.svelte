<script lang="ts">
  import type { Snippet } from "svelte";

  import Button from "$lib/components/display/button.svelte";
  import Tag from "$lib/components/display/tag.svelte";
  import {
    arraysCompare,
    markdownToHTML,
    htmlToMarkdown,
  } from "$lib/utils/misc";

  interface Props {
    value?: any;
    onUseValue?: () => void;
    showUseButton?: boolean;
    showModel?: boolean;
    type?: string;
    options?: any;
    paddingTop?: boolean;
    serviceValue?: any;
    subFields?: Record<
      string,
      Array<{
        label?: string;
        showModel: boolean;
        value: any;
        serviceValue: any;
        options: any;
        onUseValue?: () => void;
      }>
    >;
    children?: Snippet;
  }

  let {
    value,
    onUseValue,
    showUseButton = true,
    showModel = false,
    type = "text",
    options,
    paddingTop = false,
    serviceValue,
    subFields,
    children,
  }: Props = $props();

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
    if (subFields) {
      Object.values(subFields).forEach((fields) =>
        fields.forEach((field) => field.onUseValue && field.onUseValue())
      );
    }
  }

  let subFieldsHaveSameValue = $derived(
    subFields
      ? Object.values(subFields).every((fields) =>
          fields.every((field) => field.value === field.serviceValue)
        )
      : true
  );

  let haveSameValue = $derived(
    showModel && compare(value, serviceValue) && subFieldsHaveSameValue
  );
</script>

<div
  class:flex={showModel}
  class:flex-col={showModel}
  class:lg:flex-row={showModel}
  class:lg:gap-s32={showModel}
  class:gap-s16={showModel}
>
  <div class={showModel ? "lg:w-2/3" : ""}>
    {@render children?.()}
  </div>
  {#if showModel}
    <div
      class="gap-s12 flex flex-col-reverse lg:w-1/3 lg:flex-col"
      class:lg:pt-s40={paddingTop}
      class:lg:gap-s0={haveSameValue}
    >
      {#if haveSameValue}
        <small class="lg:pt-s8">Pas de différence</small>
      {:else}
        <div class="bg-info-light px-s12 py-s8 rounded-sm">
          {#if value === "" || value === undefined || value === null || (Array.isArray(value) && !value.length)}
            <small class="mb-s8 lg:pt-s8">Champs vide</small>
          {:else if type === "array"}
            <div class="gap-s8 flex flex-wrap">
              <ul class="ml-s20 text-gray-text-alt2 list-disc font-semibold">
                {#each value as v}
                  <li>
                    {options.find((option) => option.value === v)?.label || v}
                    {#if subFields && v in subFields}
                      <ul class="ml-s20 list-disc font-normal">
                        {#each subFields[v] as subField}
                          <li>
                            {subField.label
                              ? `${subField.label}: `
                              : ""}{subField.value}
                          </li>
                        {/each}
                      </ul>
                    {/if}
                  </li>
                {/each}
              </ul>
            </div>
          {:else if type === "files"}
            <div class="gap-s8 flex flex-wrap">
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
          <div class="lg:ml-s0 ml-auto">
            <Button label="Utiliser" small secondary onclick={handleUseValue} />
          </div>
        {/if}
      </div>
    </div>

    <hr class="-mx-s32 mt-s12 lg:hidden" />
  {/if}
</div>
