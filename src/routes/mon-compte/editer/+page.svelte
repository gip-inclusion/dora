<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import FormErrors from "$lib/components/display/form-errors.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import Form from "$lib/components/hoc/form.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import { arrowRightSIcon } from "$lib/icons";
  import { getApiURL } from "$lib/utils/api";
  import { refreshUserInfo, token, userInfo } from "$lib/utils/auth";
  import { userProfileSchema } from "$lib/validation/schemas/user-profile";

  function handleChange(validatedData) {
    phoneNumber = validatedData.phoneNumber;
  }

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/profile/change/`;
    const { phoneNumber } = validatedData;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
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
    await refreshUserInfo();
    goto("/mon-compte");
  }

  let requesting = false;
  let { firstName, lastName, email, phoneNumber } = $userInfo;
</script>

<EnsureLoggedIn>
  <FormErrors />

  <div class="lg:w-2/3">
    <Form
      data={{ firstName, lastName, email, phoneNumber }}
      schema={userProfileSchema}
      onChange={handleChange}
      onSubmit={handleSubmit}
      onSuccess={handleSuccess}
      bind:requesting
    >
      <Fieldset title="Informations" noTopPadding>
        <BasicInputField
          id="firstName"
          schema={userProfileSchema.firstName}
          bind:value={firstName}
          placeholder="Aurélien"
          disabled
          vertical
        />

        <BasicInputField
          id="lastName"
          schema={userProfileSchema.lastName}
          bind:value={lastName}
          placeholder="Durand"
          disabled
          vertical
        />

        <BasicInputField
          id="email"
          schema={userProfileSchema.email}
          bind:value={email}
          placeholder="nom.prenom@organisation.fr"
          disabled
          vertical
        />

        <BasicInputField
          type="tel"
          id="phoneNumber"
          schema={userProfileSchema.phoneNumber}
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
