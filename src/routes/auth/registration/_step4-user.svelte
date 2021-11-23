<script>
  import { formErrors } from "$lib/validation.js";
  import { passwordRules } from "$lib/auth";
  import { accountSchema } from "$lib/schemas/auth.js";
  import { getApiURL } from "$lib/utils/api.js";

  import Button from "$lib/components/button.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Alert from "$lib/components/forms/alert.svelte";

  import { registrationInfo } from "./_store.js";

  export let currentStep;
  let requesting = false;
  let hasAgreedToLegalMentions = false;

  const serverErrors = {
    // eslint-disable-next-line
    email: {
      invalid:
        "Cet utilisateur existe déjà.&nbsp;<a target='_blank' rel='noopener nofollow' class='underline' href='https://itou.typeform.com/doracontactsupp'>Nous contacter</a>.",
    },
  };

  const toggleText =
    "En cochant cette case je suis d’accord avec les <a class='underline' href='/mentions-legales'>mentions légales</a> et l’utilisation de mes données afin de créer un compte sur la plateforme DORA.";

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/register-structure-and-user/`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        firstName: validatedData.firstName,
        lastName: validatedData.lastName,
        email: validatedData.email,
        password: validatedData.password,
        siret: validatedData.siret,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }
  function handleSuccess() {
    currentStep = 5;
  }
</script>

<div class="col-span-full md:col-start-6 md:col-end-13 mb-s32">
  <Form
    data={$registrationInfo}
    schema={accountSchema}
    serverErrorsDict={serverErrors}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset
      title="Informations personnelles"
      description="Merci de renseigner les informations nécessaires à la création de votre compte."
    >
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert iconOnLeft label={msg} />
      {/each}
      <div class="relative flex flex-col gap-y-s32">
        <Field
          name="firstName"
          errorMessages={$formErrors.firstName}
          label="Votre prénom"
          vertical
          type="text"
          required
          placeholder="Aurélien"
          autocomplete="given-name"
          bind:value={$registrationInfo.firstName}
        />

        <Field
          name="lastName"
          errorMessages={$formErrors.lastName}
          label="Votre nom"
          vertical
          type="text"
          required
          placeholder="Durand"
          autocomplete="family-name"
          bind:value={$registrationInfo.lastName}
        />

        <Field
          name="email"
          errorMessages={$formErrors.email}
          label="Courriel"
          vertical
          type="email"
          required
          placeholder="Votre courriel"
          autocomplete="email"
          bind:value={$registrationInfo.email}
          allowHTMLError
        />
        <div class="flex flex-col md:flex-row justify-between gap-x-s32">
          <Field
            name="password"
            errorMessages={$formErrors.password}
            label="Mot de passe"
            vertical
            type="password"
            placeholder="••••••••"
            bind:value={$registrationInfo.password}
            autocomplete="new-password"
            passwordrules={passwordRules}
            required
          />
          <Field
            name="password2"
            errorMessages={$formErrors.password2}
            label="Confirmer"
            vertical
            type="password"
            placeholder="••••••••"
            bind:value={$registrationInfo.password2}
            autocomplete="new-password"
            passwordrules={passwordRules}
            required
          />
        </div>
        <Field name="siret" type="hidden" value={$registrationInfo.siret} />

        <Field
          vertical
          type="toggle"
          bind:value={hasAgreedToLegalMentions}
          toggleYesText={toggleText}
          toggleNoText={toggleText}
          placeholder=""
        />

        <Button
          type="submit"
          label="Demandez votre accès"
          disabled={!hasAgreedToLegalMentions || requesting}
          preventDefaultOnMouseDown
        />
      </div></Fieldset
    >
  </Form>
</div>
