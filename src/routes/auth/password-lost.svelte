<script>
  import { getApiURL } from "$lib/utils/api.js";

  import { formErrors } from "$lib/validation.js";

  import { passwordLostSchema } from "$lib/schemas/auth.js";

  import Button from "$lib/components/button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Alert from "$lib/components/forms/alert.svelte";
  import Form from "$lib/components/forms/form.svelte";

  let email = "";

  let success = false;
  let requesting = false;

  const authErrors = {
    _default: {},
    // eslint-disable-next-line
    nonFieldErrors: { authorization: "Courriel ou mot de passe incorrects" },
  };

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/password/reset/`;
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

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Réinitialiser votre mot de passe</h1>
  </div>
</CenteredGrid>

{#if success}
  Vérifiez votre boite mail
{:else}
  <CenteredGrid gridRow="2" roundedbg>
    <div class="col-start-5 col-end-9 mb-4">
      <Form
        data={{ email }}
        schema={passwordLostSchema}
        serverErrorsDict={authErrors}
        onChange={handleChange}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        bind:requesting>
        <Fieldset>
          <div>
            {#each $formErrors.nonFieldErrors || [] as msg}
              <Alert iconOnLeft label={msg} />
            {/each}
          </div>
          <Field
            name="email"
            errorMessages={$formErrors.email}
            label="Courriel"
            vertical
            type="email"
            placeholder="email"
            bind:value={email}
            autocomplete="current-password"
            required />

          <Button
            type="submit"
            disabled={!email || requesting}
            label="Envoyer" />
        </Fieldset>
      </Form>
    </div>
  </CenteredGrid>
{/if}
