<script>
  import { get } from "svelte/store";

  import { formErrors } from "$lib/validation.js";
  import { modifyUserSchema } from "$lib/schemas/dashboard.js";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/auth";

  import Button from "$lib/components/button.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/modal.svelte";

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
  export let member;
  export let onRefresh;

  let level = member.isAdmin ? "admin" : "user";

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/structure-members/${member.id}/`;
    return fetch(url, {
      method: "PATCH",
      body: JSON.stringify({
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
  }
</script>

<Modal bind:isOpen title="Utilisateur">
  <Form
    data={{ level }}
    schema={modifyUserSchema}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
  >
    <Fieldset>
      <Field
        name="name"
        label="Nom"
        vertical
        type="text"
        value={member.user.fullName}
        disabled
      />
      <Field
        name="email"
        label="Courriel"
        vertical
        type="email"
        value={member.user.email}
        disabled
      />
      <Field
        name="level"
        errorMessages={$formErrors.level}
        label="Permissions"
        vertical
        type="select"
        bind:value={level}
        choices={levelChoices}
        required
      />
    </Fieldset>

    <div class="mt-s32 flex flex-row justify-end gap-s16">
      <Button type="submit" label="Modifier" preventDefaultOnMouseDown />
    </div>
  </Form>
</Modal>
