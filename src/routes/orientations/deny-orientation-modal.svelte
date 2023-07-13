<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import * as v from "$lib/validation/schema-utils";
  import Button from "$lib/components/display/button.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import { denyOrientation } from "$lib/utils/orientation";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import type { Orientation } from "$lib/types";
  import ConfirmationBloc from "./confirmation-bloc.svelte";

  export let isOpen = false;
  export let onRefresh;
  export let orientation: Orientation;

  let showConfirmation = false;

  let otherDetails = "";
  let reasons: string[] = [];
  let requesting = false;

  const denyOrientationSchema: v.Schema = {
    reasons: {
      label: "Merci de cocher le ou les motifs de refus de la demande",
      default: [],
      required: true,
      rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    },
    otherDetails: {
      label: "Détaillez ici le motif du refus",
      default: "",
      rules: [v.isString(), v.maxStrLength(1000)],
      required: false,
      maxLength: 1000,
    },
  };
  const reasonChoices = [
    {
      value: "bénéficiaire-non-joignable",
      label: "Bénéficiaire non joignable",
    },
    {
      value: "bénéficiaire-absent",
      label: "Bénéficiaire ne s’étant pas présenté à l’entretien",
    },
    {
      value: "bénéficiaire-en-emploi",
      label: "Bénéficiaire indisponible : en emploi",
    },
    {
      value: "bénéficiaire-en-formation",
      label: "Bénéficiaire indisponible : en formation",
    },
    {
      value: "bénéficiaire-non-éligible",
      label: "Bénéficiaire non éligible (ne répond pas aux pré-requis)",
    },
    {
      value: "bénéficiaire-non-mobile",
      label: "Bénéficiaire non mobile",
    },
    {
      value: "bénéficiaire-non-intéressé",
      label: "Bénéficiaire non intéressé",
    },
    {
      value: "freins-périphériques",
      label:
        "Un ou plusieurs freins périphériques empêchent le bénéficiaire de poursuivre",
    },
    {
      value: "session-complète",
      label: "Session complète",
    },
    {
      value: "orientation-en-doublon",
      label: "Orientation en doublon",
    },
    {
      value: "autre",
      label: "Autre (détails dans le message ci-dessous)",
    },
  ];

  function handleSubmit(validatedData) {
    return denyOrientation(orientation.queryId, validatedData);
  }

  async function handleSuccess(_jsonResult) {
    await onRefresh();

    showConfirmation = true;
  }

  $: formData = { reasons, otherDetails };
  $: denyOrientationSchema.otherDetails.required = reasons.includes("autre");
</script>

<Modal
  bind:isOpen
  on:close
  title="Refuser la demande"
  overflow
  width="medium"
  hideTitle={showConfirmation}
>
  <div slot="subtitle">
    Vous êtes sur le point de refuser une demande de prescription de service qui
    vous a été adressée par {orientation.beneficiaryFirstName}
    {orientation.beneficiaryLastName} de la structure {orientation
      .prescriberStructure?.name}
    pour le service «&nbsp;<a
      class="text-magenta-cta"
      href="/services/{orientation.service?.slug}"
    >
      {orientation.service?.name}
    </a>&nbsp;».<br />
    <div class="mt-s16">
      Le ou la bénéficiaire, {orientation.beneficiaryFirstName}
      {orientation.beneficiaryLastName}, sera informé•e de la décision par {orientation.referentFirstName}
      {orientation.referentLastName}.
    </div>
  </div>

  {#if showConfirmation}
    <ConfirmationBloc
      title="Votre réponse a été transmise"
      subtitle="Le prescripteur sera informé par e-mail de votre décision."
      withThunder
    />
  {:else}
    <div class="pr-s16">
      <Form
        bind:data={formData}
        schema={denyOrientationSchema}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        bind:requesting
      >
        <div class="mx-s4 mb-s20">
          <CheckboxesField
            id="reasons"
            choices={reasonChoices}
            bind:value={reasons}
            vertical
          />
        </div>
        {#if reasons.includes("autre")}
          <div class="mx-s4">
            <TextareaField
              id="otherDetails"
              bind:value={otherDetails}
              vertical
            />
          </div>
        {/if}

        <div class="mt-s32 text-right">
          <Button
            name="validate"
            type="submit"
            label="Refuser la demande"
            disabled={requesting}
          />
        </div>
      </Form>
    </div>
  {/if}
</Modal>
