<script>
  import { page } from "$app/stores";

  import { getApiURL } from "$lib/utils/api.js";
  import { formErrors } from "$lib/validation.js";
  import { currentEmailSchema } from "$lib/schemas/auth.js";
  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Form from "$lib/components/forms/form.svelte";

  import Info from "$lib/components/info.svelte";
  import AuthLayout from "./_auth_layout.svelte";

  let email = $page.url.searchParams.get("email") || "";

  let success = false;
  let requesting = false;

  const authErrors = {
    _default: {},
    nonFieldErrors: { authorization: "Courriel ou mot de passe incorrects" },
  };

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/registration/resend-validation-email/`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        email: validatedData.email,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  function handleSuccess(_result) {
    success = true;
  }
</script>

<svelte:head>
  <title>Renvoyer un email de validation | DORA</title>
</svelte:head>

<CenteredGrid topPadded>
  <div class="col-span-full col-start-1 mb-s48 text-center">
    <h1 class="text-france-blue">Créer son compte DORA</h1>
  </div>
</CenteredGrid>

<AuthLayout>
  <Form
    data={{ email }}
    schema={currentEmailSchema}
    serverErrorsDict={authErrors}
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Fieldset title="Renvoyer un email de validation">
      {#if success}
        <Info label="C’est tout bon !" positiveMood>
          <p>
            Si vous avez un compte DORA avec cette adresse, vous allez recevoir
            un e-mail contenant un lien pour le valider.
          </p>
        </Info>
      {:else}
        {#if $formErrors.nonFieldErrors}
          <div>
            {#each $formErrors.nonFieldErrors || [] as msg}
              <Alert label={msg} />
            {/each}
          </div>
        {/if}

        <Field
          name="email"
          errorMessages={$formErrors.email}
          label="Courriel"
          vertical
          type="email"
          placeholder="Courriel utilisé lors de l’inscription"
          bind:value={email}
          autocomplete="current-password"
          required
        />

        <Button
          type="submit"
          disabled={!email || requesting}
          label="Valider votre compte"
          preventDefaultOnMouseDown
        />
      {/if}
    </Fieldset>
  </Form>
</AuthLayout>
