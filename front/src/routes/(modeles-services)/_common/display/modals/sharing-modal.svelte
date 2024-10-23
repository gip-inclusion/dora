<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/utils/auth";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import * as v from "$lib/validation/schema-utils";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import type { Service } from "$lib/types";
  import { trackServiceShare } from "$lib/utils/stats";
  import { page } from "$app/stores";

  export let isOpen = false;
  export let service: Service;
  export let isDI = false;

  let senderName: string;
  let recipientEmail: string | undefined;
  let recipientKind: string = "beneficiary";
  let requesting = false;
  let messageSent = false;
  let mobilisableByBeneficiary = true;

  const recipientKinds = [
    { value: "beneficiary", label: "Bénéficiaire" },
    { value: "professional", label: "Professionnel" },
  ];

  const feedbackSchema: v.Schema = {
    senderName: {
      label: "Votre nom",
      default: "",
      rules: [v.isString(), v.maxStrLength(254)],
      post: [v.trim],
      required: () => {
        return !$token;
      },
    },
    recipientEmail: {
      label: "Courriel du destinataire",
      default: "",
      rules: [v.isEmail(), v.maxStrLength(254)],
      post: [v.lower, v.trim],
      required: true,
    },
    recipientKind: {
      label: "Profil du destinataire",
      default: "beneficiary",
      rules: [v.isString()],
      required: true,
    },
  };

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/services${isDI ? "-di" : ""}/${
      service.slug
    }/share/`;
    const headers = new Headers({
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
    });
    if ($token) {
      headers.append("Authorization", `Token ${$token}`);
    }

    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        ...validatedData,
      }),
      headers,
    });
  }

  function handleSuccess(_jsonResult) {
    const searchId = $page.url.searchParams.get("searchId");
    trackServiceShare(
      service,
      recipientEmail,
      recipientKind,
      $page.url,
      searchId,
      isDI
    );
    messageSent = true;
  }

  function handleClose() {
    messageSent = false;
    senderName = undefined;
    recipientEmail = "";
    recipientKind = "beneficiary";
  }

  $: formData = {
    senderName: senderName,
    recipientEmail,
    recipientKind,
  };
  $: mobilisableByBeneficiary =
    !!service.beneficiariesAccessModes?.length ||
    !!service.beneficiariesAccessModesOther;
</script>

<Modal
  bind:isOpen
  width="medium"
  title="Partager cette fiche"
  subtitle="Envoyez cette fiche à un bénéficiaire ou à un autre professionnel."
  on:close={handleClose}
>
  {#if messageSent}
    <Notice
      type="success"
      title="La fiche a été transmise à votre destinataire."
      showIcon={false}
    ></Notice>
  {:else}
    <Form
      bind:data={formData}
      schema={feedbackSchema}
      onChange={handleChange}
      onSubmit={handleSubmit}
      onSuccess={handleSuccess}
      bind:requesting
    >
      <fieldset class="mb-s24 flex flex-col gap-s24">
        {#if !$token}
          <BasicInputField
            type="email"
            id="senderName"
            bind:value={senderName}
            description="Exemple : Nadia Comaneci"
            autocomplete="name"
            vertical
          />
        {/if}
        <BasicInputField
          type="email"
          id="recipientEmail"
          bind:value={recipientEmail}
          description="Format attendu : nom@domaine.fr."
          vertical
        />
        <RadioButtonsField
          id="recipientKind"
          bind:value={recipientKind}
          choices={recipientKinds}
          vertical
        />
      </fieldset>
      {#if !mobilisableByBeneficiary}
        <div class="mb-s24">
          <Notice
            type="warning"
            title="Ce service ne peut pas être mobilisé par le bénéficiaire"
            showIcon={false}
          >
            <p>
              Le bénéficiaire pourra consulter le service, mais il n'aura pas
              accès aux informations de contact. Seul un professionnel de
              l'insertion est habilité à orienter un bénéficiaire vers ce
              service.
            </p>
          </Notice>
        </div>
      {/if}
      <div class="flex justify-end">
        <Button
          type="submit"
          label="Envoyer la fiche"
          disabled={!recipientEmail || !recipientKind || requesting}
          preventDefaultOnMouseDown
        />
      </div>
    </Form>
  {/if}
</Modal>
