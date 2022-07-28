<script>
  import { onMount } from "svelte";
  import { getApiURL } from "$lib/utils/api.js";
  import { formErrors } from "$lib/validation.js";
  import { siretRegexp, isString, isSiret, trim } from "$lib/schemas/utils";

  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Button from "$lib/components/button.svelte";
  import Input from "$lib/components/forms/input.svelte";
  import Form from "$lib/components/forms/form.svelte";

  export let onEstablishmentChange = null;
  export let siret = "";

  let requesting = false;
  let siretIsValid = false;

  $: siretIsValid = !!siret?.match(siretRegexp);

  const siretSearchSchema = {
    siret: {
      default: "",
      required: true,
      rules: [isString(), isSiret()],
      post: [trim],
    },
  };

  const serverErrors = {
    // eslint-disable-next-line
    nonFieldErrors: { not_found: "Numéro Siret non reconnu." },
  };

  async function siretSearch(s) {
    const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(s)}`;

    return fetch(url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  async function handleSubmit(validatedData) {
    if (onEstablishmentChange) onEstablishmentChange({});

    return siretSearch(validatedData.siret);
  }

  function handleSuccess(establishment) {
    if (onEstablishmentChange) onEstablishmentChange(establishment);
  }

  onMount(async () => {
    if (siret) {
      requesting = true;
      const response = await siretSearch(siret);

      if (response.status === 200) {
        const establishment = await response.json();
        handleSuccess(establishment);
      } else {
        siret = "";
      }
      requesting = false;
    }
  });
</script>

<Form
  data={{ siret }}
  schema={siretSearchSchema}
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
          bind:value={siret}
        />
      </div>
      {#if requesting}
        <p class="py-s12 px-s8 lg:px-s20">Chargement…</p>
      {:else}
        <Button label="Rechercher" disabled={!siretIsValid} type="submit" />
      {/if}
    </div>
  </Field>
</Form>
