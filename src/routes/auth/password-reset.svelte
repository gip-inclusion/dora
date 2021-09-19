<script context="module">
  import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";

  export async function load({ page, _fetch, _session, _context }) {
    const token = page.query.get("token");
    const url = `${getApiURL()}/auth/token/verify/`;
    const result = await fetch(url, {
      method: "POST",
      headers: {
        Accept: defaultAcceptHeader,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ key: token }),
    });
    const resetToken = result.ok ? token : null;

    return {
      props: { resetToken },
    };
  }
</script>

<script>
  import { formErrors } from "$lib/validation.js";

  import { pwChangeSchema } from "$lib/schemas/auth.js";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Form from "$lib/components/forms/form.svelte";

  import connexionPic from "$lib/assets/illu_connexion-optimise.svg";

  import { passwordRules } from "$lib/auth";
  import Info from "./_info.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  export let resetToken;

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

<style>
  li {
    list-style-position: inside;
    list-style-type: disc;
  }
</style>

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Réinitialiser votre mot de passe</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="col-start-1 col-end-7 mb-4 mt-6">
    <img src={connexionPic} alt="" />
  </div>
  <div class="col-start-7 col-end-12 mb-4">
    <div class="col-start-5 col-end-11 mb-4">
      <Form
        data={{ password1, password2 }}
        schema={pwChangeSchema}
        serverErrorsDict={authErrors}
        onChange={handleChange}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}>
        <Fieldset
          title="Nouveau mot de passe"
          description="Pour réinitialiser votre mot de passe, saisissez un nouveau mot de passe et confirmez.">
          {#if !resetToken}
            <Info label="Le lien a expiré ou n’est pas valide" negativeMood />
            <LinkButton
              to="/auth/password-lost"
              label="Demander un nouveau lien"
              preventDefaultOnMouseDown />
          {:else if success}
            <Info label="C’est tout bon !" positiveMood>
              <p>
                Vous pouvez maintenant vous connecter avec le nouveau mot de
                passe.
              </p>
            </Info>
            <LinkButton
              to="/auth/login"
              label="Revenir à la page de connexion"
              preventDefaultOnMouseDown />
          {:else}
            {#if $formErrors.nonFieldErrors}
              <div>
                {#each $formErrors.nonFieldErrors || [] as msg}
                  <Alert iconOnLeft label={msg} />
                {/each}
              </div>
            {/if}
            <Field
              name="password1"
              errorMessages={$formErrors.password1}
              label="Nouveau mot de passe"
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
              label="Confirmer"
              vertical
              type="password"
              placeholder="••••••••"
              bind:value={password2}
              autocomplete="new-password"
              passwordrules={passwordRules}
              required />
            <Info>
              <p class="mb-2">
                Votre mot de passe doit respecter quelques règles :
              </p>
              <ul>
                <li>9 caractères ou plus</li>
                <li>Pas entièrement numérique</li>
              </ul>
            </Info>
            <Button
              type="submit"
              disabled={!password1 || !password2}
              label="Modifier le mot de passe"
              preventDefaultOnMouseDown />
            <p class=" text-center text-gray-text-alt2 text-xs">
              Vous vous souvenez de votre mot de passe ?
              <a class="underline " href="/auth/login">Connexion</a>
            </p>
          {/if}
        </Fieldset>
      </Form>
    </div>
  </div></CenteredGrid>
