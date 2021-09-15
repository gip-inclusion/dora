<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { getApiURL } from "$lib/utils/api.js";
  import { token, setToken } from "$lib/auth";

  import { formErrors } from "$lib/validation.js";

  import { loginSchema } from "$lib/schemas/auth.js";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Form from "$lib/components/forms/form.svelte";

  const next = $page.query.get("next") || "/";

  let email = "";
  let password = "";

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

  function handleSuccess(jsonResult) {
    setToken(jsonResult.token);
    goto(next || "/");
  }

  onMount(() => {
    if ($token && $page.path === "/auth/login") {
      goto(next);
    }
  });
</script>

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Se connecter à DORA</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="col-start-4 col-end-11 mb-4">
    <Form
      data={{ email, password }}
      schema={loginSchema}
      serverErrorsDict={authErrors}
      onChange={handleChange}
      onSubmit={handleSubmit}
      onSuccess={handleSuccess}>
      <Fieldset title="Accédez à votre compte">
        {#each $formErrors.nonFieldErrors || [] as msg}
          <Alert iconOnLeft label={msg} />
        {/each}

        <Field
          name="email"
          errorMessages={$formErrors.email}
          label="Courriel"
          vertical
          type="email"
          bind:value={email}
          required
          placeholder="Courriel"
          autocomplete="email" />
        <Field
          name="password"
          errorMessages={$formErrors.password}
          label="Mot de passe"
          vertical
          type="password"
          placeholder="••••••••"
          bind:value={password}
          autocomplete="current-password"
          required />
        <Button
          type="submit"
          disabled={!email || !password}
          label="Se connecter"
          preventDefaultOnMouseDown />
        <a
          class="underline text-center text-gray-text-alt2 text-xs"
          href="/auth/password-lost">Mot de passe oublié ?</a>
      </Fieldset>
    </Form>
  </div>
</CenteredGrid>
