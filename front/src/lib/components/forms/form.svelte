<script lang="ts" context="module">
  export interface FormControls {
    submit?: (submitterId?: string) => Promise<void>;
    validateForm?: (submitterId?: string) => {
      valid: boolean;
      validatedData: any;
    };
  }
</script>

<script lang="ts">
  import type { Snippet } from "svelte";
  import { onDestroy, onMount, setContext } from "svelte";

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

  let hasUnsavedChange = false;
  interface Props {
    data: any;
    schema: Schema;
    requesting?: boolean;
    serverErrorsDict?: any;
    onSubmit: any;
    onSuccess: (jsonResult: any, submitterId?: string) => void;
    servicesOptions?: ServicesOptions;
    onChange?: (validatedData, fieldName?) => void;
    disableExitWarning?: boolean;
    onValidate?: (
      submittedData,
      submitterId?: string
    ) => { validatedData; valid: boolean };
    children?: Snippet;
    formControls?: FormControls;
  }

  let {
    data = $bindable(),
    schema,
    requesting = $bindable(false),
    serverErrorsDict = {},
    onSubmit,
    onSuccess,
    servicesOptions,
    onChange,
    disableExitWarning = false,
    onValidate,
    children,
    formControls = $bindable({}),
  }: Props = $props();

  $effect(() => {
    $currentFormData = data;
  });

  $effect(() => {
    $currentSchema = schema;
  });

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
            noScroll: true,
            servicesOptions,
          }
        );
        if (valid && onChange) {
          onChange(validatedData, fieldName);
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
    } catch {
      jsonResult = null;
    }
    return jsonResult;
  }

  function runValidation(submitterId?: string) {
    $formErrors = {};
    return onValidate
      ? onValidate(data, submitterId)
      : validate(data, schema, { servicesOptions });
  }

  async function submitForm(submitterId?: string) {
    const { validatedData, valid } = runValidation(submitterId);
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
          requesting = false;
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
        requesting = false;
        throw err;
      }
    }
  }

  formControls = { submit: submitForm, validateForm: runValidation };

  async function handleSubmit(event: Event) {
    event.preventDefault();
    const submitterId = (event as SubmitEvent).submitter?.id;
    await submitForm(submitterId);
  }
</script>

<form onsubmit={handleSubmit} novalidate>
  {@render children?.()}
</form>
