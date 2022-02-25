<script>
  import { getApiURL } from "$lib/utils/api.js";
  import { formErrors } from "$lib/validation.js";
  import * as v from "$lib/schemas/utils";

  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Button from "$lib/components/button.svelte";
  import Input from "$lib/components/forms/input.svelte";
  import Form from "$lib/components/forms/form.svelte";

  export let onEstablishmentChange = null;

  let siretCode = "";
  let searching = false;
  let siretIsValid = false;

  $: siretIsValid = !!siretCode.match(/^\d{14}$/u);

  const siretSearchSchema = {
    siretCode: {
      default: "",
      required: true,
      rules: [v.isString(), v.isSiret()],
      post: [v.trim],
    },
  };

  const serverErrors = {
    // eslint-disable-next-line
    nonFieldErrors: { not_found: "Numéro SIRET non reconnu." },
  };

  async function handleSubmit(validatedData) {
    if (onEstablishmentChange) onEstablishmentChange({});

    const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(
      validatedData.siretCode
    )}`;

    return fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  function handleSuccess(result) {
    if (onEstablishmentChange) onEstablishmentChange(result);

    searching = false;
  }
</script>

<Form
  data={{ siretCode }}
  schema={siretSearchSchema}
  serverErrorsDict={serverErrors}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
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
    label="Numéro Siret"
    required
    vertical
    description="Sur 14 chiffres"
  >
    <div slot="custom-input" class="flex gap-s12">
      <div class="flex grow">
        <Input
          type="text"
          name="siret-select"
          placeholder="1234567891234"
          bind:value={siretCode}
        />
      </div>
      {#if searching}
        <p class="py-s12 px-s8 lg:px-s20">Chargement…</p>
      {:else}
        <Button label="Rechercher" disabled={!siretIsValid} type="submit" />
      {/if}
    </div>
  </Field>
</Form>
