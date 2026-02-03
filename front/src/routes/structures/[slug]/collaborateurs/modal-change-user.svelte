<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { getToken } from "$lib/utils/auth";
  import { modifyUserSchema } from "$lib/validation/schemas/dashboard";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";

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
  interface Props {
    isOpen?: boolean;
    member: any;
    onRefresh: any;
  }

  let {
    isOpen = $bindable(false),
    member = $bindable(),
    onRefresh,
  }: Props = $props();

  let level = $state(member.isAdmin ? "admin" : "user");

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
        Authorization: `Token ${getToken()}`,
      },
    });
  }

  async function handleSuccess(_jsonResult) {
    await onRefresh();
    isOpen = false;
  }

  let formData = $derived({ level });
</script>

<Modal bind:isOpen title="Utilisateur">
  <Form
    bind:data={formData}
    schema={modifyUserSchema}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    disableExitWarning
  >
    <Fieldset noTopPadding>
      <BasicInputField
        id="name"
        disabled
        vertical
        value={member.user.fullName}
      />
      <BasicInputField
        type="email"
        id="email"
        disabled
        vertical
        value={member.user.email}
      />
      <SelectField
        id="level"
        vertical
        bind:value={level}
        choices={levelChoices}
      />
    </Fieldset>

    <div class="mt-s32 gap-s16 flex flex-row justify-end">
      <Button type="submit" label="Modifier" preventDefaultOnMouseDown />
    </div>
  </Form>
</Modal>
