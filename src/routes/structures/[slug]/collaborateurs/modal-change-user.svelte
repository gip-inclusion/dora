<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Form from "$lib/components/hoc/form.svelte";
  import Modal from "$lib/components/display/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/utils/auth";
  import { modifyUserSchema } from "$lib/validation/schemas/dashboard";
  import { get } from "svelte/store";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
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
  export let member;
  export let onRefresh;

  let level = member.isAdmin ? "admin" : "user";

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
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
  >
    <Fieldset noTopPadding>
      <BasicInputField
        id="name"
        schema={modifyUserSchema.name}
        vertical
        value={member.user.fullName}
      />
      <BasicInputField
        type="email"
        id="email"
        schema={modifyUserSchema.email}
        vertical
        value={member.user.email}
      />
      <SelectField
        id="level"
        schema={modifyUserSchema.level}
        vertical
        bind:value={level}
        choices={levelChoices}
      />
    </Fieldset>

    <div class="mt-s32 flex flex-row justify-end gap-s16">
      <Button type="submit" label="Modifier" preventDefaultOnMouseDown />
    </div>
  </Form>
</Modal>
