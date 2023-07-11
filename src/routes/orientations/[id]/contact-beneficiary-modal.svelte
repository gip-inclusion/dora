<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import * as v from "$lib/validation/schema-utils";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import Button from "$lib/components/display/button.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import { contactBeneficiary } from "$lib/utils/orientation";
  import type { Orientation } from "$lib/types";
  import ConfirmationBloc from "./confirmation-bloc.svelte";

  export let isOpen = false;
  export let onRefresh;
  export let orientation: Orientation;

  let showConfirmation = false;

  let message = "";
  let extraRecipients = [];
  let requesting = false;

  const contactBeneficiarySchema: v.Schema = {
    extraRecipients: {
      label: "Ajouter d‘autres destinataires",
      default: [],
      rules: [],
    },
    message: {
      label: "Votre message",
      default: "",
      rules: [v.isString(), v.maxStrLength(1000)],
      required: true,
      maxLength: 1000,
    },
  };
  const extraRecipientsChoices = [
    {
      value: "add-service-contact",
      label: "Ajouter en copie le prescripteur ou la prescriptrice",
    },
    {
      value: "add-referent-contact",
      label: "Ajouter en copie le conseiller ou la conseillère référente",
    },
  ];

  function handleSubmit(validatedData) {
    return contactBeneficiary(
      orientation.queryId,
      validatedData.extraRecipients,
      validatedData.message
    );
  }

  async function handleSuccess(_jsonResult) {
    await onRefresh();
    showConfirmation = true;
  }

  $: formData = { extraRecipients, message };
</script>

<Modal
  bind:isOpen
  on:close
  overflow
  title="Contacter le ou la bénéficiaire"
  width="medium"
>
  <div slot="subtitle">
    Contacter {orientation.beneficiaryFirstName}
    {orientation.beneficiaryLastName} - qui vous a été adressé·e par {orientation.referentFirstName}
    {orientation.referentLastName}, pour le service «&nbsp;<a
      class="text-magenta-cta"
      href="/services/{orientation.service?.slug}"
    >
      {orientation.service?.name}
    </a>&nbsp;»
  </div>

  {#if showConfirmation}
    <ConfirmationBloc title="Votre message a été transmis" />
  {:else}
    <div class="pr-s16">
      <Form
        bind:data={formData}
        schema={contactBeneficiarySchema}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        bind:requesting
      >
        <div class="mx-s4 mb-s20">
          <CheckboxesField
            id="extraRecipients"
            choices={extraRecipientsChoices}
            bind:value={extraRecipients}
            hideLabel
            vertical
          />
        </div>
        <div class="mx-s4">
          <TextareaField id="message" bind:value={message} vertical />
        </div>

        <div class="mt-s32 text-right">
          <Button
            name="validate"
            type="submit"
            label="Envoyer le message"
            disabled={requesting}
          />
        </div>
      </Form>
    </div>
  {/if}
</Modal>
