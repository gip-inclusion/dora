<script>
  import { goto } from "$app/navigation";
  import { token } from "$lib/auth";
  import { getApiURL } from "$lib/utils/api.js";
  import { passwordChangeSchema } from "$lib/schemas/auth";
  import { passwordRules } from "$lib/auth";
  import { formErrors } from "$lib/validation.js";

  import Button from "$lib/components/button.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Info from "$lib/components/info.svelte";
  import SchemaField from "$lib/components/forms/schema-field.svelte";

  import { arrowRightSIcon, lightBulbIcon } from "$lib/icons";

  const authErrors = {
    _default: {},
    // eslint-disable-next-line
    nonFieldErrors: {
      // eslint-disable-next-line
      password_too_similar:
        "Le mot de passe est trop semblable à votre nom ou à votre adresse courriel",
      // eslint-disable-next-line
      permission_denied: "Mot de passe actuel incorrect",
    },
  };

  let success = false;
  let requesting = false;
  let currentPassword, newPassword1, newPassword2;

  function handleChange(_validatedData) {
    success = false;
  }

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/profile/password/change/`;
    return fetch(url, {
      method: "POST",
      body: JSON.stringify({
        currentPassword: validatedData.currentPassword,
        newPassword: validatedData.newPassword1,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });
  }

  function handleSuccess(_result) {
    success = true;
    currentPassword = newPassword1 = newPassword2 = "";

    goto("/mon-compte");
  }
</script>

<Form
  data={{ currentPassword, newPassword1, newPassword2 }}
  schema={passwordChangeSchema}
  serverErrorsDict={authErrors}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  <Fieldset title="Mot de passe">
    {#if $formErrors.nonFieldErrors}
      <div>
        {#each $formErrors.nonFieldErrors || [] as msg}
          <Alert label={msg} />
        {/each}
      </div>
    {/if}
    <div>
      <SchemaField
        name="currentPassword"
        errorMessages={$formErrors.currentPassword}
        schema={passwordChangeSchema.currentPassword}
        label="Mot de passe actuel"
        vertical
        type="password"
        placeholder="••••••••"
        bind:value={currentPassword}
        autocomplete="new-password"
        passwordrules={passwordRules}
      />
      <a
        class="block text-right text-f12 text-gray-text-alt2 underline"
        href="/auth/mdp-perdu">Mot de passe oublié ?</a
      >
    </div>
    <SchemaField
      name="newPassword1"
      errorMessages={$formErrors.newPassword1}
      schema={passwordChangeSchema.newPassword1}
      label="Nouveau mot de passe"
      vertical
      type="password"
      placeholder="••••••••"
      bind:value={newPassword1}
      autocomplete="new-password"
      passwordrules={passwordRules}
    />
    <Info label="">
      <div>
        <p class="legend mb-s16">
          Votre mot de passe doit respecter quelques règles :
        </p>
        <ul class="legend list-outside list-disc pl-s16">
          <li>9 caractères ou plus</li>
          <li>Pas entièrement numérique</li>
        </ul>
      </div>
    </Info>
    <SchemaField
      name="newPassword2"
      errorMessages={$formErrors.newPassword2}
      schema={passwordChangeSchema.newPassword2}
      label="Confirmer le nouveau mot de passe"
      vertical
      type="password"
      placeholder="••••••••"
      bind:value={newPassword2}
      autocomplete="new-password"
      passwordrules={passwordRules}
    />

    {#if success}
      <Info
        icon={lightBulbIcon}
        label="Votre nouveau mot de passe à été enregistré avec succès !"
        positiveMood
      />
    {/if}

    <div class="self-end">
      <Button
        type="submit"
        disabled={!newPassword1 || !newPassword2}
        label="Valider"
        iconOnRight
        icon={arrowRightSIcon}
        preventDefaultOnMouseDown
      />
    </div>
  </Fieldset>
</Form>
