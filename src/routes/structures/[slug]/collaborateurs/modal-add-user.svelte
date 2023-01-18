<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Form from "$lib/components/hoc/form.svelte";
  import Modal from "$lib/components/display/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/utils/auth";
  import { addUserSchema } from "$lib/validation/schemas/dashboard";
  import { get } from "svelte/store";
  import ConfirmationModal from "./modal-confirmation.svelte";
  import FormErrors from "$lib/components/display/form-errors.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import SelectField from "$lib/components/inputs/select-field.svelte";

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

  let email: string;
  let level: "user" | "admin" = "user";
  let successEmailMsg;
  let confirmationModalIsOpen = false;
  let requesting = false;

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
    level = "user";
    confirmationModalIsOpen = true;
  }
</script>

<Modal bind:isOpen title="Nouveau collaborateur">
  <FormErrors />

  <Form
    data={{ email, level }}
    schema={addUserSchema}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset noTopPadding>
      <BasicInputField
        type="email"
        id="email"
        bind:value={email}
        schema={addUserSchema.email}
        vertical
        placeholder="nom@exemple.org"
      />

      <SelectField
        id="level"
        schema={addUserSchema.level}
        vertical
        bind:value={level}
        choices={levelChoices}
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
