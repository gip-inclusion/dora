<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import { getApiURL } from "$lib/utils/api.js";
  import { token, setToken, validateCredsAndFillUserInfo } from "$lib/auth";
  import { formErrors } from "$lib/validation.js";
  import { loginSchema } from "$lib/schemas/auth.js";

  import Button from "$lib/components/button.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import Info from "$lib/components/info.svelte";
  import AuthLayout from "./_auth_layout.svelte";
  import Notice from "$lib/components/notice.svelte";

  let email = "";
  let password = "";
  let invalidUser = false;

  const authErrors = {
    _default: {},
    nonFieldErrors: { authorization: "Courriel ou mot de passe incorrects" },
  };

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/login/`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        email: validatedData.email,
        password: validatedData.password,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  function getNextPage() {
    const next = $page.url.searchParams.get("next");
    if (next && next.startsWith("/") && !next.startsWith("/auth/")) return next;
    return "/";
  }

  async function handleSuccess(jsonResult) {
    if (jsonResult.validUser) {
      setToken(jsonResult.token);
      await validateCredsAndFillUserInfo();

      goto(getNextPage() || "/");
    } else {
      invalidUser = true;
    }
  }

  onMount(() => {
    if ($token && $page.url.pathname === "/auth/connexion") {
      goto(getNextPage());
    }
  });
</script>

<svelte:head>
  <title>Se connecter | DORA</title>
</svelte:head>

<CenteredGrid>
  <div class="text-center">
    <h1 class="text-france-blue">Connexion</h1>
  </div>
</CenteredGrid>

<AuthLayout>
  <div class="mb-s40">
    <Form
      data={{ email, password }}
      schema={loginSchema}
      serverErrorsDict={authErrors}
      onChange={handleChange}
      onSubmit={handleSubmit}
      onSuccess={handleSuccess}
    >
      <Fieldset title="Votre compte">
        {#if invalidUser}
          <Info
            label="Votre adresse courriel n’a pas encore été validée"
            negativeMood
          />
          <LinkButton
            to="/auth/renvoyer-email-validation?email={encodeURIComponent(
              email
            )}"
            label="Demander un nouveau lien"
          />
        {:else}
          {#each $formErrors.nonFieldErrors || [] as msg}
            <Alert label={msg} />
          {/each}
          <div class="mb-s16 flex flex-col md:flex-row md:gap-s16 lg:flex-col">
            <Field
              name="email"
              errorMessages={$formErrors.email}
              label="Courriel"
              vertical
              type="email"
              bind:value={email}
              required
              placeholder="Courriel utilisé lors de l’inscription"
              autocomplete="email"
            />
            <Field
              name="password"
              errorMessages={$formErrors.password}
              label="Mot de passe"
              vertical
              type="password"
              placeholder="••••••••"
              bind:value={password}
              autocomplete="current-password"
              required
            />
          </div>

          <div class="flex flex-col">
            <Button
              type="submit"
              disabled={!email || !password}
              label="Se connecter"
              preventDefaultOnMouseDown
            />
          </div>
          <div class="mt-s16">
            <a
              class="text-center text-f12 text-gray-text-alt2 underline"
              href="/auth/mdp-perdu">Mot de passe oublié ?</a
            >
          </div>
        {/if}
      </Fieldset>
    </Form>
  </div>

  <Notice title="Vous n'avez pas encore de compte ?">
    <LinkButton
      slot="button"
      label="Créer un compte"
      secondary
      nofollow
      small
      to={`/auth/inscription`}
    />
  </Notice>
</AuthLayout>
