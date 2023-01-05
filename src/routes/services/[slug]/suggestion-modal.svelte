<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Form from "$lib/components/display/form.svelte";
  import Modal from "$lib/components/display/modal.svelte";
  import Field from "$lib/components/inputs/field.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { userInfo } from "$lib/utils/auth";
  import { suggestionSchema } from "$lib/validation/schemas/service";
  import { formErrors } from "$lib/validation/validation";
  import { onMount } from "svelte";
  import SuggestionConfirmationModal from "./suggestion-confirmation-modal.svelte";

  export let isOpen = false;
  export let service;

  let message, suggesterFullName, suggesterEmail;
  let confirmationModalIsOpen = false;
  let requesting = false;

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

  async function handleSuccess(_jsonResult) {
    isOpen = false;
    message = null;
    confirmationModalIsOpen = true;
  }
</script>

<Modal bind:isOpen title="Suggestion">
  <Form
    data={{ fullName: suggesterFullName, email: suggesterEmail, message }}
    schema={suggestionSchema}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset>
      {#if !$userInfo}
        <Field
          name="fullName"
          errorMessages={$formErrors.fullName}
          label="Nom"
          vertical
          type="text"
          placeholder="Aurélien Durand"
          bind:value={suggesterFullName}
          required
          autocomplete="name"
        />

        <Field
          name="email"
          errorMessages={$formErrors.email}
          label="Courriel"
          vertical
          type="email"
          bind:value={suggesterEmail}
          required
          placeholder="nom@exemple.org"
          autocomplete="email"
        />
      {/if}
      <Field
        name="message"
        errorMessages={$formErrors.message}
        label="Message"
        description="Détaillez les éléments qui vous semblent erronés ou incomplets."
        vertical
        type="textarea"
        rows="6"
        bind:value={message}
        required
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
<SuggestionConfirmationModal bind:isOpen={confirmationModalIsOpen} />
