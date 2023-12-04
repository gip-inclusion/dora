<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/utils/auth";
  import { addUserSchema } from "$lib/validation/schemas/dashboard";
  import { get } from "svelte/store";
  import ConfirmationModal from "./modal-confirmation.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";

  const USER_LEVEL_CHOICES = [
    {
      value: "user",
      label: "Utilisateur (saisie d’offres, modification profil)",
    },
    {
      value: "admin",
      label:
        "Administrateur (saisie d’offres, modification profil, édition de la structure, gestion des utilisateurs)",
    },
  ] as const;
  type userLevelKind = (typeof USER_LEVEL_CHOICES)[number]["value"];

  export let isOpen = false;
  export let structure;
  export let members;
  export let onRefresh;
  export let suggestAdmin = false;

  let email = "";
  let level: userLevelKind = suggestAdmin ? "admin" : "user";

  let successEmailMsg;
  let confirmationModalIsOpen = false;
  let requesting = false;

  function handleSubmit(validatedData) {
    const membersEmails = members.map((member) => member.user.email);
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

    email = "";

    confirmationModalIsOpen = true;
  }

  $: formData = { email, level, siret: structure.siret };
</script>

<Modal bind:isOpen title="Nouveau collaborateur">
  <FormErrors />

  <Form
    bind:data={formData}
    schema={addUserSchema}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    disableExitWarning
    bind:requesting
  >
    <Fieldset noTopPadding>
      <BasicInputField
        type="email"
        id="email"
        bind:value={email}
        vertical
        placeholder="nom@exemple.org"
      />

      <SelectField
        id="level"
        vertical
        bind:value={level}
        choices={USER_LEVEL_CHOICES}
        placeholder="Permissions"
      />
    </Fieldset>
    <div class="mt-s32 flex flex-row justify-end gap-s16">
      <Button
        type="submit"
        label="Envoyer l’invitation"
        disabled={!email || !level || requesting}
        preventDefaultOnMouseDown
      />
    </div>
  </Form>
</Modal>

<ConfirmationModal
  bind:isOpen={confirmationModalIsOpen}
  email={successEmailMsg}
/>
