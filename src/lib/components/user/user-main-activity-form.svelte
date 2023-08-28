<script lang="ts">
  import { onMount } from "svelte";

  import Form from "$lib/components/forms/form.svelte";
  import * as v from "$lib/validation/schema-utils";
  import { refreshUserInfo, userInfo } from "$lib/utils/auth";
  import Button from "$lib/components/display/button.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import { updateUserMainActivity } from "$lib/utils/user";

  let userMainActivity = "";
  let requesting = false;

  export let onSuccess;

  const userMainActivityOptions = [
    {
      value: "accompagnateur",
      label:
        "Je consulte les offres d‘insertion de mon territoire dans le but de rester informé•e des opportunités existantes et accompagner/orienter mes bénéficiaires",
    },
    {
      value: "offreur",
      label: "Je référence l‘offre de service de ma ou mes structures sur DORA",
    },
    {
      value: "accompagnateur_offreur",
      label:
        "Les deux : je consulte les offres de mon territoire et je référence l‘offre de service de ma ou mes structures",
    },
    {
      value: "autre",
      label: "Autre",
    },
  ];

  const userMainActivitySchema: v.Schema = {
    userMainActivity: {
      label: "Quels sont vos objectifs lors de l’utilisation de DORA ?",
      default: "",
      rules: [v.isString(), v.maxStrLength(255)],
      required: true,
    },
  };

  onMount(() => {
    if ($userInfo) {
      userMainActivity = $userInfo.mainActivity;
    }
  });

  async function handleSubmit(validatedData) {
    await updateUserMainActivity(validatedData.userMainActivity);
    await refreshUserInfo();
    return { ok: true };
  }

  function handleSuccess(_jsonResult) {
    if (onSuccess) {
      onSuccess();
    }
  }

  $: formData = { userMainActivity };
</script>

<Form
  bind:data={formData}
  schema={userMainActivitySchema}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  <div class="mx-s4">
    <RadioButtonsField
      id="userMainActivity"
      choices={userMainActivityOptions}
      description="Veuillez choisir la réponse qui correspond le mieux à votre utilisation actuelle (ou future, si vous venez de vous inscrire)."
      bind:value={userMainActivity}
      vertical
    />
  </div>

  <div class="mt-s32 text-right">
    <Button
      name="validate"
      type="submit"
      label="Valider"
      disabled={requesting}
    />
  </div>
</Form>
