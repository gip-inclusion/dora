<script>
  import { get } from "svelte/store";

  import { formErrors } from "$lib/validation.js";
  import { addUserSchema } from "$lib/schemas/dashboard.js";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/auth";

  import Button from "$lib/components/button.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/modal.svelte";
  import ConfirmationModal from "./_confirmation-modal.svelte";

  const levelChoices = [
    {
      value: "user",
      label: "Utilisateur (saisie d’offres, modification profil)",
    },
    {
      value: "admin",
      label:
        "Administrateur (saisie d’offres, modification profil, édition de la structure, gestion des utilisateurs)",
    },
  ];
  export let isOpen = false;
  export let structure;
  export let members;
  export let onRefresh;

  let firstName, lastName, email;
  let level = "user";
  let successEmailMsg;
  let confirmationModalIsOpen = false;
  let requesting = false;

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const membersEmails = members.map((m) => m.user.email);
    if (membersEmails.includes(validatedData.email)) {
      return {
        ok: false,
        json: () => ({
          email: [
            { message: "Cet utilisateur fait déjà partie de votre structure" },
          ],
        }),
      };
    }
    const url = `${getApiURL()}/structure-putative-members/?structure=${
      structure.slug
    }`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        user: {
          firstName: validatedData.firstName,
          lastName: validatedData.lastName,
          email: validatedData.email,
        },
        isAdmin: validatedData.level === "admin",
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
        Authorization: `Token ${get(token)}`,
      },
    });
  }

  async function handleSuccess(_jsonResult) {
    await onRefresh();
    isOpen = false;
    successEmailMsg = email;
    firstName = null;
    lastName = null;
    email = null;
    level = "user";
    confirmationModalIsOpen = true;
  }
</script>

<Modal bind:isOpen>
  <Form
    data={{ firstName, lastName, email, level }}
    schema={addUserSchema}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset title="Nouveau collaborateur" noTopPadding>
      <Field
        name="firstName"
        errorMessages={$formErrors.firstName}
        label="Prénom"
        vertical
        type="text"
        placeholder="Aurélien"
        bind:value={firstName}
        required
      />
      <Field
        name="lastName"
        errorMessages={$formErrors.lastName}
        label="Nom"
        vertical
        type="text"
        placeholder="Durand"
        bind:value={lastName}
        required
      />

      <Field
        name="email"
        errorMessages={$formErrors.email}
        label="Courriel"
        vertical
        type="email"
        bind:value={email}
        required
        placeholder="nom@exemple.org"
      />

      <Field
        name="level"
        errorMessages={$formErrors.level}
        label="Niveau"
        vertical
        type="select"
        bind:value={level}
        choices={levelChoices}
        required
        placeholder="Permissions"
      />
      <Button
        type="submit"
        label="Envoyer l’invitation"
        disabled={!firstName || !lastName || !email || !level || requesting}
        preventDefaultOnMouseDown
      />
    </Fieldset>
  </Form>
</Modal>
<ConfirmationModal
  bind:isOpen={confirmationModalIsOpen}
  email={successEmailMsg}
/>
