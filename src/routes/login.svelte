<script>
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { getApiURL } from "$lib/utils";
  import { token, setToken } from "$lib/auth";
  import { onMount } from "svelte";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";

  const next = $page.query.get("next") || "/";

  let email = "";
  let password = "";

  async function handleSubmit() {
    const url = `${getApiURL()}/api-token-auth/`;
    const result = await fetch(url, {
      method: "POST",
      body: JSON.stringify({
        username: email,
        password,
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
    }
    return {
      status: result.status,
      error: new Error(`Could not load ${url}`),
    };
  }

  function validateMessageEmail(event) {
    const textbox = event.target;
    if (textbox.value === "") {
      textbox.setCustomValidity("Ce champ est requis");
    } else if (textbox.validity.typeMismatch) {
      textbox.setCustomValidity(
        "Merci de renseigner une adresse de couriel valide"
      );
    } else {
      textbox.setCustomValidity("");
    }
    return true;
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
    <form on:submit|preventDefault={handleSubmit}>
      <Fieldset title="Accédez à votre compte">
        <Field
          label="Courriel"
          vertical
          type="email"
          bind:value={email}
          on:invalid={validateMessageEmail}
          required
          placeholder="Courriel" />
        <Field
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
          label="Votre nom"
          vertical
          type="text"
          required
          placeholder="Votre nom" />
        <Field
          label="Votre prénom"
          vertical
          type="text"
          required
          placeholder="Votre prénom" />
      </div>
      <div class="flex flex-row justify-between gap-x-4">
        <Field
          label="Courriel"
          vertical
          type="email"
          required
          placeholder="Votre courriel" />
        <Field
          label="Téléphone"
          vertical
          type="tel"
          placeholder="Votre numéro de téléphone" />
      </div>
      <div class="flex flex-row justify-between gap-x-4">
        <Field
          label="Nom de votre structure"
          vertical
          type="text"
          required
          placeholder="Votre structure" />
        <Field
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
