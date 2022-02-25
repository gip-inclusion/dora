<script>
  import { userInfo, refreshUserInfo, token } from "$lib/auth";
  import { getApiURL } from "$lib/utils/api.js";
  import { userProfileSchema } from "$lib/schemas/auth";
  import { formErrors } from "$lib/validation.js";

  import Button from "$lib/components/button.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import Info from "$lib/components/info.svelte";

  import { arrowRightSIcon, lightBulbIcon } from "$lib/icons";

  const authErrors = {};
  let success = false;

  function handleChange(_validatedData) {
    success = false;
  }

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/profile/change/`;
    const { firstName, lastName, newsletter, phoneNumber } = validatedData;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        firstName,
        lastName,
        newsletter,
        phoneNumber,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });
  }

  async function handleSuccess(_result) {
    success = true;
    await refreshUserInfo();
  }

  let requesting = false;
  let { firstName, lastName, email, phoneNumber } = $userInfo;
  // At the moment we don't want to expose this field
  const newsletter = $userInfo.newsletter;

  $: infoIsMissing = !firstName || !lastName || !email || !phoneNumber;
  $: infoChanged =
    firstName !== $userInfo?.firstName ||
    lastName !== $userInfo?.lastName ||
    email !== $userInfo?.email ||
    phoneNumber !== $userInfo?.phoneNumber;
</script>

<Form
  data={{ firstName, lastName, email, phoneNumber, newsletter }}
  schema={userProfileSchema}
  serverErrorsDict={authErrors}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  <Fieldset title="Vos informations et coordonnées">
    <ModelField
      name="firstName"
      errorMessages={$formErrors.firstName}
      schema={userProfileSchema.firstName}
      label="Prénom"
      vertical
      type="text"
      placeholder="Aurélien"
      bind:value={firstName}
    />
    <ModelField
      name="lastName"
      errorMessages={$formErrors.lastName}
      schema={userProfileSchema.lastName}
      label="Nom"
      vertical
      type="text"
      placeholder="Durand"
      bind:value={lastName}
    />
    <ModelField
      name="email"
      errorMessages={$formErrors.email}
      schema={userProfileSchema.email}
      label="Courriel"
      vertical
      type="email"
      bind:value={email}
      placeholder="email_pro@e-mail.com"
      disabled
    />

    <ModelField
      name="phoneNumber"
      errorMessages={$formErrors.phoneNumber}
      schema={userProfileSchema.phoneNumber}
      label="Numéro de téléphone"
      vertical
      type="email"
      bind:value={phoneNumber}
      placeholder="0X XX XX XX XX"
    />

    {#if success}
      <Info
        icon={lightBulbIcon}
        label="Vos informations personnelles ont été mises à jour&nbsp!"
        positiveMood
      />
    {/if}

    <div class="self-end">
      <Button
        type="submit"
        label="Validez les informations"
        disabled={requesting || infoIsMissing || !infoChanged}
        iconOnRight
        icon={arrowRightSIcon}
        preventDefaultOnMouseDown
      />
    </div>
  </Fieldset>
</Form>
