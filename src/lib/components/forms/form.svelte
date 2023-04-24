<script lang="ts">
  import { beforeNavigate } from "$app/navigation";
  import type { ServicesOptions } from "$lib/types";
  import type { Schema } from "$lib/validation/schema-utils";
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
  export let onChange: ((validatedData) => void) | undefined = undefined;
  export let disableExitWarning = false;

  let hasUnsavedChange = false;
  export let onValidate:
    | ((
        submittedData,
        submitterId: string | undefined
      ) => { validatedData; valid: boolean })
    | undefined = undefined;

  $: $currentFormData = data;
  $: $currentSchema = schema;

  onMount(() => {
    $formErrors = {};
  });

  beforeNavigate((navigation) => {
    if (
      hasUnsavedChange &&
      !disableExitWarning &&
      // eslint-disable-next-line
      !window.confirm(
        "Cette page demande de confirmer sa fermeture; des données saisies pourraient ne pas être enregistrées."
      )
    ) {
      return navigation.cancel();
    }
    return null;
  });

  onDestroy(() => {
    $formErrors = {};
  });

  async function handleEltChange(evt) {
    $formErrors.nonFieldErrors = [];

    // We want to listen to both DOM and component events
    const fieldName = evt.target?.name || evt.detail;

    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated, although it's not
    // supposed to happen. This setTimeout is an unsatisfying workaround to that.
    await new Promise((resolve) => {
      setTimeout(() => {
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

        hasUnsavedChange = true;
        resolve(true);
      }, 200);
    });
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
    const submitterId = (event as SubmitEvent).submitter?.id;
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
          // `onSuccess` pouvant faire une redirection et activer la fenêtre d'avertissement,
          // `hasUnsavedChange` doit être modifié avant `onSuccess`
          hasUnsavedChange = false;

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
