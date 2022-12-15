<script lang="ts">
  import RichText from "$lib/components/inputs/rich-text/editor.svelte";
  import FieldWrapper from "./field-wrapper.svelte";

  export let label: string;
  export let name: string;
  export let value: string;
  export let placeholder = "";
  export let helper = "";
  export let maxlength: number | undefined = undefined;
  export let disabled = false;
  export let required = false;
  export let rows: number | undefined = 3;
  export let inputType:
    | "text"
    | "textarea"
    | "url"
    | "email"
    | "hidden"
    | "richtext"
    | "tel" = "text";

  export let errorMessages: string[] = [];
  let ariaDescribedBy = "";

  // AriaDescribedBy => TODO: move to wrapper
  $: {
    ariaDescribedBy = helper ? `${name}-helper` : "";
    if ((errorMessages || []).length) {
      ariaDescribedBy = `${ariaDescribedBy} ${name}-error`;
    }
  }

  // Props
  $: props = {
    id: name,
    name,
    disabled,
    required,
    maxlength,
    placeholder,
    "aria-describedby": ariaDescribedBy,
    class: `rounded rounded border bg-white p-s12 font-sans disabled:bg-gray-bg disabled:text-gray-text ${
      errorMessages?.length > 0 ? "border-error" : "border-gray-03"
    }`,
  };
</script>

<FieldWrapper
  {label}
  {name}
  {helper}
  {required}
  {errorMessages}
  hidden={inputType === "hidden"}
>
  {#if inputType === "textarea"}
    <textarea bind:value on:blur on:input {...props} {rows} />
  {:else if inputType === "url"}
    <input type="url" bind:value on:blur on:input {...props} />
  {:else if inputType === "email"}
    <input type="email" bind:value on:blur on:input {...props} />
  {:else if inputType === "tel"}
    <input type="tel" bind:value on:blur on:input {...props} />
  {:else if inputType === "hidden"}
    <input type="hidden" bind:value disabled />
  {:else if inputType === "richtext"}
    <RichText
      bind:htmlContent={value}
      initialContent={value}
      id="{name}-rich-text"
      {disabled}
      {name}
      {placeholder}
      {ariaDescribedBy}
    />
  {:else}
    <input type="text" bind:value on:blur on:input {...props} />
  {/if}
</FieldWrapper>
