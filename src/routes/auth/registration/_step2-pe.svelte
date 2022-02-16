<script>
  import { getApiURL } from "$lib/utils/api.js";
  import { formErrors } from "$lib/validation.js";
  import { arrowLeftSIcon } from "$lib/icons.js";
  import { safirSearchSchema } from "$lib/schemas/auth.js";

  import Form from "$lib/components/forms/form.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Button from "$lib/components/button.svelte";
  import Toggle from "$lib/components/toggle.svelte";
  import Alert from "$lib/components/forms/alert.svelte";

  import { registrationInfo } from "./_store.js";

  export let currentStep;
  let structure;
  let safirCode;

  const serverErrors = {
    // eslint-disable-next-line
    nonFieldErrors: { not_found: "Code SAFIR inconnu." },
  };

  let structureVisible = false;
  let hasCheckedConsent = false;

  function handleJoin() {
    $registrationInfo.siret = structure.siret;
    $registrationInfo.isPoleEmploi = true;
    currentStep = 4;
  }

  function handleBackButton() {
    if (structureVisible) {
      structure = null;
      structureVisible = false;
      safirCode = "";
    } else {
      currentStep = 1;
    }
  }

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
    structure = result;
    structureVisible = true;
  }
</script>

<Form
  data={{ safirCode }}
  schema={safirSearchSchema}
  serverErrorsDict={serverErrors}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
>
  <FieldSet
    title="Votre structure"
    description="Vous avez declaré être attaché a une agence Pôle Emploi. Merci de renseigner le code SAFIR de votre agence afin de l’identifier."
  >
    {#if $formErrors.nonFieldErrors?.length}
      <div>
        {#each $formErrors.nonFieldErrors || [] as msg}
          <Alert label={msg} />
        {/each}
      </div>
    {/if}
    <Field
      name="safirCode"
      errorMessages={$formErrors.safirCode}
      label="Code SAFIR"
      vertical
      type="text"
      placeholder="Code numérique correspondant à votre structure"
      bind:value={safirCode}
      required
    />

    {#if structure && structureVisible}
      <div class="establishment-details">
        <h4 class="text-gray-text">{structure.name}</h4>
        <div class="legend">{structure.address1}</div>
        <div class="legend">{structure.address2}</div>
        <div class="legend">
          {structure.postalCode}
          {structure.city}
        </div>
      </div>
      <div class="flex">
        <Toggle
          toggleYesText=""
          toggleNoText=""
          bind:checked={hasCheckedConsent}
        />
        <div class="legend">
          En cochant cette case, je déclare faire partie de la structure
          mentionnée ci-dessus et j’atteste connaître les risques encourus en
          cas de faux et d’usage de faux.
        </div>
      </div>
    {/if}

    <div class="flex flex-col items-start md:flex-row md:justify-between">
      <Button
        label="Retour"
        on:click={handleBackButton}
        icon={arrowLeftSIcon}
        noPadding
        noBackground
      />
      {#if !structureVisible}
        <Button
          type="submit"
          label="Chercher la structure"
          disabled={!safirCode}
          preventDefaultOnMouseDown
        />
      {:else}
        <Button
          label="Adhérez à la structure"
          disabled={!hasCheckedConsent}
          on:click={handleJoin}
          preventDefaultOnMouseDown
        />
      {/if}
    </div>
  </FieldSet>
</Form>

<style lang="postcss">
  .establishment-details {
    padding: var(--s24);
    border: 1px solid var(--col-gray-01);
  }
</style>
