<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { userInfo } from "$lib/utils/auth";
  import { onMount } from "svelte";
  import FeedbackConfirmationModal from "./feedback-confirmation-modal.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import * as v from "$lib/validation/schema-utils";

  export let isOpen = false;
  export let service;

  let message, suggesterFullName, suggesterEmail;
  let confirmationModalIsOpen = false;
  let requesting = false;

  const feedbackSchema: v.Schema = {
    fullName: {
      label: "Nom",
      default: "",
      rules: [v.isString(), v.maxStrLength(140)],
      post: [v.trim],
      required: true,
    },
    email: {
      label: "Courriel",
      default: "",
      rules: [v.isEmail(), v.maxStrLength(254)],
      post: [v.lower, v.trim],
      required: true,
    },
    message: {
      label: "Message",
      default: "",
      rules: [v.isString()],
      required: true,
    },
  };

  onMount(() => {
    if ($userInfo) {
      suggesterFullName = $userInfo.fullName;
      suggesterEmail = $userInfo.email;
    }
  });

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/services/${service.slug}/feedback/`;

    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        ...validatedData,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  function handleSuccess(_jsonResult) {
    isOpen = false;
    message = null;
    confirmationModalIsOpen = true;
  }

  $: formData = {
    fullName: suggesterFullName,
    email: suggesterEmail,
    message,
  };
</script>

<Modal bind:isOpen title="Suggestion">
  <Form
    bind:data={formData}
    schema={feedbackSchema}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset>
      {#if !$userInfo}
        <BasicInputField
          id="fullName"
          bind:value={suggesterFullName}
          vertical
          placeholder="Aurélien Durand"
          autocomplete="name"
        />

        <BasicInputField
          type="email"
          id="email"
          bind:value={suggesterEmail}
          placeholder="nom.prenom@organisation.fr"
          autocomplete="email"
          vertical
        />
      {/if}

      <TextareaField
        id="message"
        bind:value={message}
        description="Détaillez les éléments qui vous semblent erronés ou incomplets."
        vertical
        rows={6}
        placeholder="Renseigner ici les détails"
      />
    </Fieldset>
    <p class="mt-s24">
      <small>
        Vos informations de contact sont transmises à l’équipe Dora pour des
        fins de traitement.<br />L'administrateur du service reçoit uniquement
        votre message.
      </small>
    </p>
    <div class="mt-s32 flex justify-end">
      <Button
        type="submit"
        label="Envoyer"
        disabled={!suggesterEmail ||
          !suggesterFullName ||
          !message ||
          requesting}
        preventDefaultOnMouseDown
      />
    </div>
  </Form>
</Modal>
<FeedbackConfirmationModal bind:isOpen={confirmationModalIsOpen} />
