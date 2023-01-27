<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import { arrowRightSIcon } from "$lib/icons";
  import { getApiURL } from "$lib/utils/api";
  import { refreshUserInfo, token, userInfo } from "$lib/utils/auth";
  import { userProfileSchema } from "$lib/validation/schemas/user-profile";

  let requesting = false;
  let { firstName, lastName, email, phoneNumber } = $userInfo;

  function handleChange(validatedData) {
    phoneNumber = validatedData.phoneNumber;
  }

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/profile/change/`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        phoneNumber: validatedData.phoneNumber,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });
  }

  async function handleSuccess(_result) {
    await refreshUserInfo();
    goto("/mon-compte");
  }

  $: formData = { firstName, lastName, email, phoneNumber };
</script>

<EnsureLoggedIn>
  <FormErrors />

  <div class="lg:w-2/3">
    <Form
      bind:data={formData}
      schema={userProfileSchema}
      onChange={handleChange}
      onSubmit={handleSubmit}
      onSuccess={handleSuccess}
      bind:requesting
    >
      <Fieldset title="Informations" noTopPadding>
        <BasicInputField
          id="firstName"
          bind:value={firstName}
          placeholder="Aurélien"
          disabled
          vertical
        />

        <BasicInputField
          id="lastName"
          bind:value={lastName}
          placeholder="Durand"
          disabled
          vertical
        />

        <BasicInputField
          id="email"
          bind:value={email}
          placeholder="nom.prenom@organisation.fr"
          disabled
          vertical
        />

        <BasicInputField
          type="tel"
          id="phoneNumber"
          bind:value={phoneNumber}
          placeholder="0X XX XX XX XX"
          vertical
        />
      </Fieldset>

      <div class="mt-s32 flex flex-col justify-end gap-s16 md:flex-row ">
        <Button
          type="submit"
          label="Valider"
          disabled={requesting}
          iconOnRight
          icon={arrowRightSIcon}
          preventDefaultOnMouseDown
        />
      </div>
    </Form>
  </div>
</EnsureLoggedIn>
