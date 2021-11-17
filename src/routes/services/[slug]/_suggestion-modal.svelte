<script>
  import { get } from "svelte/store";

  import { formErrors } from "$lib/validation.js";
  import { suggestionSchema } from "$lib/schemas/service";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/auth";

  import Button from "$lib/components/button.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/modal.svelte";
  import SuggestionConfirmationModal from "./_suggestion_confirmation_modal.svelte";

  export let isOpen = false;
  export let service;

  let fullName, email, message;
  let confirmationModalIsOpen = false;
  let requesting = false;

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
        Authorization: `Token ${get(token)}`,
      },
    });
  }

  async function handleSuccess(_jsonResult) {
    isOpen = false;
    fullName = null;
    email = null;
    message = null;
    confirmationModalIsOpen = true;
  }
</script>

<Modal bind:isOpen>
  <Form
    data={{ fullName, email, message }}
    schema={suggestionSchema}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset
      title="Suggérer une modification"
      description="Vos informations de contact seront transmises à l’équipe Dora pour des fins de traitement – le partenaire (auteur de la fiche) recevra uniquement votre message."
      noTopPadding
    >
      <Field
        name="fullName"
        errorMessages={$formErrors.fullName}
        label="Votre nom complet"
        vertical
        type="text"
        placeholder="Aurélien Durand"
        bind:value={fullName}
        required
        autocomplete="name"
      />

      <Field
        name="email"
        errorMessages={$formErrors.email}
        label="Courriel"
        vertical
        type="email"
        bind:value={email}
        required
        placeholder="email_pro@e-mail.com"
        autocomplete="email"
      />

      <Field
        name="message"
        errorMessages={$formErrors.message}
        label="Vos propositions de modifications"
        description="Merci de détailler ici les éléments qui vous semblent erronés ou incomplets."
        vertical
        type="textarea"
        rows="6"
        bind:value={message}
        required
        placeholder="Renseigner ici les détails"
      />
      <Button
        type="submit"
        label="Envoyer la suggestion"
        disabled={!fullName || !email || !message || requesting}
        preventDefaultOnMouseDown
      />
    </Fieldset>
  </Form>
</Modal>
<SuggestionConfirmationModal bind:isOpen={confirmationModalIsOpen} />
