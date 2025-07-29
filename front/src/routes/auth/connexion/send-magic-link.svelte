<script lang="ts">
  import * as v from "$lib/validation/schema-utils";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { getApiURL } from "$lib/utils/api";

  const schema: v.Schema = {
    email: {
      label: "Votre adresse e-mail",
      default: "",
      required: true,
      rules: [v.isEmail(), v.maxStrLength(254)],
      post: [v.lower, v.trim],
      maxLength: 254,
    },
  };

  interface Props {
    displayModal?: boolean;
  }

  let { displayModal = $bindable(false) }: Props = $props();

  let formData = $state({ email: "" });
  let displayNotice = $state(false);
  let requesting = $state(false);

  async function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/send-link/`;
    const method = "POST";
    const result = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
      },
      body: new URLSearchParams(validatedData),
    });
    return result;
  }

  function handleSuccess() {
    displayNotice = true;
  }

  function handleNewRequest() {
    displayNotice = false;
    formData = { email: "" };
  }
</script>

<Modal
  bind:isOpen={displayModal}
  title="Des difficultés à vous connecter&#8239;?"
>
  <CenteredGrid>
    <p>
      Saisissez l'adresse e-mail de votre compte DORA ou de l’ancien compte
      Inclusion Connect afin de recevoir un lien temporaire d'accès à votre
      espace.
    </p>
    {#if displayNotice}
      <Notice type="success" title="Votre demande a été enregistrée">
        <p>
          Si un compte existe avec cette adresse e-mail, vous recevrez un lien
          temporaire sur cette même adresse dans quelques instants.
        </p>
      </Notice>
      <div class="mt-s32 gap-s16 flex flex-col justify-end md:flex-row">
        <Button
          name="validate"
          type="button"
          label="Faire une nouvelle demande"
          onclick={handleNewRequest}
        />
      </div>
    {:else}
      <FormErrors />
      <Form
        bind:data={formData}
        {schema}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        bind:requesting
      >
        <Fieldset>
          <BasicInputField
            type="email"
            id="email"
            bind:value={formData.email}
            placeholder="nom@domaine.fr"
            vertical
          />
        </Fieldset>
        <div class="mt-s32 gap-s16 flex flex-col justify-end md:flex-row">
          <Button
            name="validate"
            type="submit"
            label="Recevoir le lien d'accès"
            disabled={requesting}
          />
        </div>
      </Form>
    {/if}
  </CenteredGrid>
</Modal>
