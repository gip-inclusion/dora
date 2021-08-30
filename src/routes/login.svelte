<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { getApiURL } from "$lib/utils";
  import { token, setToken } from "$lib/auth";

  import { validate, formErrors, injectAPIErrors } from "$lib/validation.js";

  import authSchema from "$lib/schemas/auth.js";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";

  const next = $page.query.get("next") || "/";

  let email = "";
  let password = "";

  const authErrors = {
    _default: {},
    // eslint-disable-next-line
    non_field_errors: { authorization: "Courriel ou mot de passe incorrects" },
  };

  async function handleSubmit() {
    const { validatedData, valid } = validate(
      { email, password },
      authSchema,
      authSchema,
      { skipDependenciesCheck: true }
    );
    if (valid) {
      const url = `${getApiURL()}/api-token-auth/`;
      try {
        const result = await fetch(url, {
          method: "POST",
          body: JSON.stringify({
            username: validatedData.email,
            password: validatedData.password,
          }),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json; version=1.0",
          },
        });

        if (result.ok) {
          const jsonResult = await result.json();
          setToken(jsonResult.token);
          await goto(next || "/");
        } else {
          const jsonResult = await result.json();
          injectAPIErrors(jsonResult, authErrors);
        }
      } catch (err) {
        injectAPIErrors(
          {
            // eslint-disable-next-line
            non_field_errors: [
              { code: "fetch-error", message: "Erreur de connexion" },
            ],
          },
          authErrors
        );
      }
    }
  }

  onMount(() => {
    if ($token && $page.path === "/login") {
      goto(next);
    }
  });
  const toggleText =
    "En cochant cette case je suis d’accord avec les <a class='underline' href='/mentions-legales'>mentions légales</a> et l’utilisation de mes données afin de créer un compte sur la plateforme DORA.";
</script>

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Se connecter à DORA</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="col-start-2 col-end-6 mb-4">
    <form on:submit|preventDefault={handleSubmit} novalidate>
      <Fieldset title="Accédez à votre compte">
        {#each $formErrors.non_field_errors || [] as msg}
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
          placeholder="Courriel" />
        <Field
          name="password"
          errorMessages={$formErrors.password}
          label="Mot de passe"
          vertical
          type="password"
          placeholder="••••••••"
          bind:value={password}
          required />
        <Button
          type="submit"
          disabled={!email || !password}
          label="Se connecter" />
      </Fieldset>
    </form>
  </div>
  <div class="col-start-6 col-end-13 mb-4 ">
    <Fieldset
      title="Demandez un accès"
      description="Pour la periode de test, la création de comptes est désactivée. Contactez-nous pour obtenir un compte.">
      <div class="flex flex-row gap-x-4">
        <Field
          name="lastname"
          label="Votre nom"
          vertical
          type="text"
          required
          placeholder="Votre nom" />
        <Field
          name="firstname"
          label="Votre prénom"
          vertical
          type="text"
          required
          placeholder="Votre prénom" />
      </div>
      <div class="flex flex-row justify-between gap-x-4">
        <Field
          name="cr-courriel"
          label="Courriel"
          vertical
          type="email"
          required
          placeholder="Votre courriel" />
        <Field
          name="phone"
          label="Téléphone"
          vertical
          type="tel"
          placeholder="Votre numéro de téléphone" />
      </div>
      <div class="flex flex-row justify-between gap-x-4">
        <Field
          name="struct-name"
          label="Nom de votre structure"
          vertical
          type="text"
          required
          placeholder="Votre structure" />
        <Field
          name="siret"
          label="Le numéro SIRET"
          vertical
          type="text"
          required
          placeholder="SIRET" />
      </div>
      <Field
        vertical
        type="toggle"
        toggleYesText={toggleText}
        toggleNoText={toggleText}
        placeholder="" />

      <Button type="button" label="Demandez votre accès" disabled />
    </Fieldset>
  </div>
</CenteredGrid>
