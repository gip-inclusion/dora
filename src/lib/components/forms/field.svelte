<script>
  import Input from "./input.svelte";
  import Label from "./label.svelte";
  import Alert from "./alert.svelte";

  export let value = undefined;
  export let selectedItem = undefined;

  export let type;
  export let errors;
  export let errorMessages;

  export let vertical = false;
  export let label = "";
  export let required = false;
  export let maxLength = undefined;
  export let choices = [];

  export let disabled = undefined;
  export let visible = true;
  export let placeholder = "";
  export let description = "";
  export let minValue = null;

  export let hideLabel = false;
  export let toggleYesText;
  export let toggleNoText;

  let validity;
  let validityError;

  let layoutClass = vertical ? "flex-col " : "flex-row";
  $: hiddenClasses = type === "hidden" ? "hidden" : "";

  let currentErrorMessage;

  $: if (errors) {
    currentErrorMessage = errorMessages
      ? errorMessages[errors.errorCode]
      : errors.errorMessage;
  } else {
    currentErrorMessage = "";
  }

  $: console.log(currentErrorMessage);

  function handleInvalid(elt) {
    validity = elt.target.validity;
    let type = elt.target.type;
    console.log(type, validity);
    if (!validity.valid) {
      if (validity.valueMissing) {
        validityError = "Ce champ est requis";
      }
      if (type == "email" && validity.typeMismatch) {
        validityError = "Renseignez une adresse email valide";
      }
      if (type == "url" && validity.typeMismatch) {
        validityError = "Renseignez une URL valide";
      }
    }
  }
</script>

<style lang="postcss">
  :global(.tag) {
    @apply bg-magenta-80 rounded px-1;
  }

  .wrapper {
    display: block;
    opacity: 1;
    transition: all 0.2s;
  }

  .invisible {
    display: none;
    opacity: 0;
    transition: all 0.2s;
  }
</style>

<div
  class:hidden={type == "hidden"}
  class:invisible={!visible}
  class="wrapper flex-1">
  <Label
    className="flex {layoutClass} items-top relative "
    isDOMLabel={type !== "checkboxes" && type !== "radios"}>
    <div
      class="flex flex-col"
      class:w-250p={!vertical}
      class:w-full={vertical}
      class:mb-1={vertical}>
      <div
        class="inline-block w-full flex-shrink-0 text-base font-bold text-gray-dark">
        {hideLabel ? "" : label}
        {#if required}<span class="text-error">*</span>{/if}
      </div>
      <span class="text-xs text-gray-text-alt2"> {description}</span>
    </div>
    <div class="flex flex-col flex-grow min-h-6 ml-4">
      <slot name="input">
        <Input
          on:invalid={handleInvalid}
          on:blur={(evt) => evt.target.checkValidity()}
          on:input
          {type}
          bind:value
          bind:selectedItem
          {required}
          {choices}
          {maxLength}
          {placeholder}
          {minValue}
          {disabled}
          {toggleYesText}
          {toggleNoText} />
      </slot>
      {#if validity && !validity.valid}
        <Alert iconOnLeft label={validityError} />
      {/if}
      {#if currentErrorMessage}
        <Alert iconOnLeft label={currentErrorMessage} />
      {/if}
    </div>
    <slot name="helptext" />
  </Label>
</div>
