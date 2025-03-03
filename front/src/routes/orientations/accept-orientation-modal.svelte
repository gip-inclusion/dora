<script lang="ts">
  import Modal from "$lib/components/hoc/modal.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import * as v from "$lib/validation/schema-utils";
  import Button from "$lib/components/display/button.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import { acceptOrientation } from "$lib/utils/orientation";
  import type { Orientation } from "$lib/types";
  import ConfirmationBloc from "./confirmation-bloc.svelte";
  import {
    renderBeneficiaryAcceptMessage,
    renderPrescriberAcceptMessage,
  } from "$lib/utils/orientation-templates";
  import { formatPhoneNumber } from "$lib/utils/misc";

  export let isOpen = false;
  export let onRefresh;
  export let orientation: Orientation;
  export let queryHash: string;

  let showConfirmation = false;

  let requesting = false;

  const acceptOrientationSchema: v.Schema = {
    message: {
      label: "Message de réponse",
      default: "",
      required: true,
      rules: [v.maxStrLength(1000)],
      maxLength: 1000,
    },
    beneficiaryMessage: {
      label: "Message pour le ou la bénéficiaire",
      default: "",
      rules: [v.maxStrLength(1000)],
      required: true,
      maxLength: 1000,
    },
  };

  function handleSubmit(validatedData) {
    return acceptOrientation(orientation.queryId, queryHash, validatedData);
  }

  async function handleSuccess(_jsonResult) {
    await onRefresh();
    showConfirmation = true;
  }

  const message = renderPrescriberAcceptMessage({
    beneficiaryFirstName: orientation.beneficiaryFirstName,
    beneficiaryLastName: orientation.beneficiaryLastName,
    serviceStructureName: orientation.service?.structureName,
    serviceContactName: orientation.service?.contactName,
    serviceContactPhone: orientation.service?.contactPhone
      ? formatPhoneNumber(orientation.service?.contactPhone)
      : undefined,
    serviceContactEmail: orientation.service?.contactEmail,
    serviceName: orientation.service?.name,
  });

  const beneficiaryMessage = renderBeneficiaryAcceptMessage({
    referentFirstName: orientation.referentFirstName,
    referentLastName: orientation.referentLastName,
    serviceName: orientation.service?.name,
    structurePhone: orientation.service?.contactPhone,
    serviceStructureName: orientation.service?.structureName,
    serviceContactName: orientation.service?.contactName,
  });

  $: formData = { message, beneficiaryMessage };
</script>

<Modal
  bind:isOpen
  on:close
  title="Valider la demande"
  hideTitle={showConfirmation}
  width="medium"
>
  <div slot="subtitle">
    Vous êtes sur le point de valider une demande d’orientation qui vous a été
    adressée par {orientation.prescriber?.name} pour le service «&nbsp;<a
      class="text-magenta-cta"
      href="/services/{orientation.service?.slug}"
    >
      {orientation.service?.name}
    </a>&nbsp;»
  </div>

  {#if showConfirmation}
    <ConfirmationBloc
      title="Votre réponse a été transmise"
      subtitle="Le prescripteur et le bénéficiaire seront informés par e-mail de votre décision. "
      withThunder
    />
  {:else}
    <div class="pr-s16">
      <Form
        bind:data={formData}
        schema={acceptOrientationSchema}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        bind:requesting
      >
        <TextareaField
          id="message"
          description="Commentaire privé à destination du prescripteur ou de la prescriptrice, ainsi que du conseiller ou de la conseillère référente s’il ne s’agit pas de la même personne. Ce message n’est pas envoyé au bénéficiaire."
          bind:value={formData.message}
          vertical
        />

        {#if orientation.beneficiaryEmail}
          <div class="mt-s20">
            <TextareaField
              id="beneficiaryMessage"
              description="Commentaire privé à destination du ou de la bénéficiaire."
              bind:value={formData.beneficiaryMessage}
              vertical
            />
          </div>
        {/if}

        <div class="mt-s32 text-right">
          <Button
            name="validate"
            type="submit"
            label="Valider la demande"
            disabled={requesting}
          />
        </div>
      </Form>
    </div>
  {/if}
</Modal>
