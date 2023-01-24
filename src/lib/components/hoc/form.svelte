<script lang="ts">
  import type { ServicesOptions } from "$lib/types";
  import type { Schema } from "$lib/validation/schemas/utils";
  import {
    contextValidationKey,
    currentFormData,
    currentSchema,
    formErrors,
    injectAPIErrors,
    validate,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { onDestroy, onMount, setContext } from "svelte";

  export let data;
  export let schema: Schema;
  export let requesting = false;
  export let serverErrorsDict = {};
  export let onSubmit, onSuccess;
  export let servicesOptions: ServicesOptions | undefined = undefined;
  export let onChange: ((data) => void) | undefined = undefined;
  export let onValidate:
    | ((
        data,
        submitterId: string | undefined
      ) => { validatedData; valid: boolean })
    | undefined = undefined;

  $: $currentFormData = data;
  $: $currentSchema = schema;

  onMount(() => {
    $formErrors = {};
  });

  onDestroy(() => {
    $formErrors = {};
  });

  async function handleEltChange(evt) {
    $formErrors.nonFieldErrors = [];

    // We want to listen to both DOM and component events
    const fieldName = evt.target?.name || evt.detail;

    const { validatedData, valid } = validate(
      data,
      { [fieldName]: schema[fieldName] },
      {
        fullFormSchema: schema,
        noScroll: true,
        servicesOptions,
      }
    );

    if (valid && onChange) {
      onChange(validatedData);
    }
  }

  setContext<ValidationContext>(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });

  async function getJsonResult(result) {
    let jsonResult;
    try {
      jsonResult = await result.json();
    } catch (err) {
      jsonResult = null;
    }
    return jsonResult;
  }

  async function handleSubmit(event: Event) {
    let submitterId = (event as SubmitEvent).submitter?.id;
    $formErrors = {};
    const { validatedData, valid } = onValidate
      ? onValidate(data, submitterId)
      : validate(data, schema, {
          servicesOptions,
        });
    if (valid) {
      try {
        requesting = true;
        const result = await onSubmit(validatedData, submitterId);
        if (result.ok) {
          await onSuccess(await getJsonResult(result), submitterId);
        } else {
          injectAPIErrors(await getJsonResult(result), serverErrorsDict);
        }
      } catch (err) {
        injectAPIErrors(
          {
            nonFieldErrors: [
              { code: "fetch-error", message: "Erreur de connexion" },
            ],
          },
          serverErrorsDict
        );
        throw err;
      } finally {
        requesting = false;
      }
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} novalidate>
  <slot />
</form>
