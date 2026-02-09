<script lang="ts">
  import { getContext, type Snippet } from "svelte";

  import { randomId } from "$lib/utils/random";
  import {
    contextValidationKey,
    formErrors,
    type ValidationContext,
  } from "$lib/validation/validation";

  import Alert from "../display/alert.svelte";

  interface Props {
    id: string;
    label?: string;
    descriptionText?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    required?: boolean;
    vertical?: boolean;
    readonly?: boolean;
    disabled?: boolean;
    description?: Snippet;
    children?: Snippet<
      [
        {
          onBlur: (evt: Event) => void;
          onChange: (evt: Event) => void;
          errorMessages: Array<string>;
        },
      ]
    >;
  }

  let {
    id,
    label = "",
    descriptionText = "",
    hidden = false,
    hideLabel = false,
    required = false,
    vertical = false,
    readonly = false,
    disabled = false,
    description,
    children,
  }: Props = $props();

  const context = getContext<ValidationContext>(contextValidationKey);

  function handleBlur(evt: Event) {
    if (context) {
      context.onBlur(evt);
    }
  }

  function handleChange(evt: Event) {
    if (context) {
      context.onChange(evt);
    }
  }

  const errorMessages = $derived($formErrors[id]);
  const descriptionId = descriptionText ? randomId() : null;
</script>

<div
  {id}
  class="field-wrapper items-top gap-s8 flex flex-col items-stretch lg:items-start"
  class:lg:flex-row={!vertical}
  class:lg:items-stretch={vertical}
  class:hidden
>
  <div class="label-container flex flex-col {!vertical ? 'lg:w-1/3' : ''}">
    <label
      for={id}
      class="mt-s8"
      class:sr-only={hideLabel}
      aria-describedby={descriptionId}
    >
      <span class="text-f17 text-gray-dark font-bold">
        {label}{#if required && !readonly && !disabled}<span
            class="ml-s6 text-error">&nbsp;*</span
          >{/if}
      </span>
    </label>
    {#if descriptionText}
      <small id={descriptionId}>{descriptionText}</small>
    {/if}
    {#if description}
      <div class="mb-s4">
        {@render description()}
      </div>
    {/if}
  </div>
  <div class="flex flex-col {!vertical ? 'lg:w-2/3' : ''}">
    {#if children}
      {@render children({
        onBlur: handleBlur,
        onChange: handleChange,
        errorMessages,
      })}
    {/if}
    {#each errorMessages || [] as msg, i}
      <Alert id="{id}-error-{i}" label={msg} />
    {/each}
  </div>
</div>
