<script>
  import { getApiURL } from "$lib/utils/api.js";
  import { formErrors } from "$lib/validation.js";

  import { safirSearchSchema } from "$lib/schemas/auth.js";

  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Button from "$lib/components/button.svelte";
  import Input from "$lib/components/forms/input.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import { safirRegexp } from "$lib/schemas/utils";

  export let onEstablishmentChange = null;

  let safirCode = "";
  let requesting = false;
  let safirIsValid = false;

  $: safirIsValid = !!safirCode.match(safirRegexp);

  const serverErrors = {
    // eslint-disable-next-line
    nonFieldErrors: { not_found: "Numéro Safir non reconnu." },
  };

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/search-safir/?safir=${validatedData.safirCode}`;
    return fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  function handleSuccess(result) {
    if (onEstablishmentChange) onEstablishmentChange(result);
  }
</script>

<Form
  data={{ safirCode }}
  schema={safirSearchSchema}
  serverErrorsDict={serverErrors}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  {#if $formErrors.nonFieldErrors?.length}
    <div>
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert label={msg} />
      {/each}
    </div>
  {/if}
  <Field
    type="custom"
    label="Numéro Safir"
    errorMessages={$formErrors.safirCode}
    required
    vertical
    description="Sur 5 chiffres"
  >
    <div slot="custom-input" class="flex gap-s12">
      <div class="flex grow">
        <Input
          type="text"
          name="safir-select"
          placeholder="12345"
          bind:value={safirCode}
        />
      </div>
      {#if requesting}
        <p class="py-s12 px-s8 lg:px-s20">Chargement…</p>
      {:else}
        <Button label="Rechercher" disabled={!safirIsValid} type="submit" />
      {/if}
    </div>
  </Field>
</Form>
