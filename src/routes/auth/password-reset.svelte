<script>
  import { page } from "$app/stores";
  import { getApiURL } from "$lib/utils/api.js";

  import { formErrors } from "$lib/validation.js";

  import { pwChangeSchema } from "$lib/schemas/auth.js";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import { passwordRules } from "$lib/auth";

  const resetToken = $page.query.get("token");

  let password1 = "";
  let password2 = "";

  let success = false;

  const authErrors = {
    _default: {},
    // eslint-disable-next-line
    nonFieldErrors: {
      // eslint-disable-next-line
      password_too_similar:
        "Le mot de passe est trop semblable à votre nom ou à votre adresse email",
    },
  };

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/password/reset/confirm/`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        newPassword: validatedData.password1,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
        Authorization: `Token ${resetToken}`,
      },
    });
  }

  function handleSuccess(_result) {
    success = true;
  }
</script>

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Réinitialiser votre mot de passe</h1>
  </div>
</CenteredGrid>

{#if !resetToken}
  Lien invalide
{:else if success}
  Mot de passe changé avec succès, vous pouvez maintenant vous <a
    href="/auth/login">connecter</a
  >.
{:else}
  <CenteredGrid gridRow="2" roundedbg>
    <div class="col-start-5 col-end-11 mb-4">
      <Form
        data={{ password1, password2 }}
        schema={pwChangeSchema}
        serverErrorsDict={authErrors}
        onChange={handleChange}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}>
        <Fieldset>
          <div>
            {#each $formErrors.nonFieldErrors || [] as msg}
              <Alert iconOnLeft label={msg} />
            {/each}
          </div>
          <Field
            name="password1"
            errorMessages={$formErrors.password1}
            label="Mot de passe"
            vertical
            type="password"
            placeholder="••••••••"
            bind:value={password1}
            autocomplete="new-password"
            passwordrules={passwordRules}
            required />
          <Field
            name="password2"
            errorMessages={$formErrors.password2}
            label="Mot de passe"
            vertical
            type="password"
            placeholder="••••••••"
            bind:value={password2}
            autocomplete="new-password"
            passwordrules={passwordRules}
            required />
          <Button
            type="submit"
            disabled={!password1 || !password2}
            label="Changer" />
        </Fieldset>
      </Form>
    </div>
  </CenteredGrid>
{/if}
