<script>
  import { setContext, onMount } from "svelte";

  import {
    validate,
    formErrors,
    injectAPIErrors,
    contextValidationKey,
  } from "$lib/validation.js";

  export let data;
  export let schema;
  export let requesting;
  export let serverErrorsDict;
  export let onSubmit, onSuccess, onChange;

  onMount(() => {
    $formErrors = {};
  });

  async function handleEltChange(evt) {
    $formErrors.nonFieldErrors = [];

    // We want to listen to both DOM and component events
    const fieldname = evt.target?.name || evt.detail;

    const filteredSchema = Object.fromEntries(
      Object.entries(schema).filter(([name, _rules]) => name === fieldname)
    );
    const { validatedData, valid } = validate(data, filteredSchema, schema, {
      skipDependenciesCheck: false,
      noScroll: true,
    });
    if (valid) {
      onChange(validatedData);
    }
  }

  setContext(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });

  async function handleSubmit() {
    $formErrors = {};

    const { validatedData, valid } = validate(data, schema, schema, {
      skipDependenciesCheck: false,
    });
    if (valid) {
      try {
        requesting = true;
        const result = await onSubmit(validatedData);
        if (result.ok) {
          onSuccess(result.status === 204 ? "" : await result.json());
        } else {
          const jsonResult = await result.json();
          injectAPIErrors(jsonResult, serverErrorsDict);
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
