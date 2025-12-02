<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { getToken } from "$lib/utils/auth";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import * as v from "$lib/validation/schema-utils";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import type { Service } from "$lib/types";
  import { trackServiceShare } from "$lib/utils/stats";
  import { page } from "$app/stores";
  import { browser } from "$app/environment";
  interface Props {
    isOpen?: boolean;
    service: Service;
    isDI?: boolean;
  }

  let { isOpen = $bindable(false), service, isDI = false }: Props = $props();

  let senderName: string | undefined = $state();
  let recipientEmail: string | undefined = $state();
  let recipientKind: string = $state("beneficiary");
  let requesting = $state(false);
  let messageSent = $state(false);

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
        return !getToken();
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
    if (getToken()) {
      headers.append("Authorization", `Token ${getToken()}`);
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

  let formData = $derived({
    senderName: senderName,
    recipientEmail,
    recipientKind,
  });

  let mobilisableByBeneficiary = $derived(
    !!service.beneficiariesAccessModes?.length ||
      !!service.beneficiariesAccessModesOther
  );
</script>

{#if browser}
  <Modal
    bind:isOpen
    width="medium"
    title="Partager cette fiche"
    subtitleText="Envoyez cette fiche à un bénéficiaire ou à un autre professionnel."
    onClose={handleClose}
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
        <fieldset class="mb-s24 gap-s24 flex flex-col">
          {#if !getToken()}
            <BasicInputField
              type="email"
              id="senderName"
              bind:value={senderName}
              descriptionText="Exemple : Nadia Comaneci"
              autocomplete="name"
              vertical
            />
          {/if}
          <BasicInputField
            type="email"
            id="recipientEmail"
            bind:value={recipientEmail}
            descriptionText="Format attendu : nom@domaine.fr."
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
{/if}
