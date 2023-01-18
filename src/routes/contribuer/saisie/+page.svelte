<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import FormErrors from "$lib/components/display/form-errors.svelte";
  import Form from "$lib/components/hoc/form.svelte";
  import { publishServiceSuggestion } from "$lib/requests/services";
  import type { Service } from "$lib/types";
  import { contribSchema } from "$lib/validation/schemas/service";

  import type { PageData } from "./$types";
  import Fields from "./fields.svelte";

  let requesting = false;

  // TODO: Ajouter le type Contribution
  let service: Service = Object.fromEntries(
    Object.entries(contribSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );

  function handleChange(validatedData) {
    console.log("change");
    service = { ...service, ...validatedData };
  }

  function handleSubmit(validatedData) {
    console.log("submit", validatedData);
    return publishServiceSuggestion(validatedData, data.source);
  }

  function handleSuccess(_result) {
    goto(`/contribuer/merci`);
  }

  export let data: PageData;
</script>

<CenteredGrid>
  <div class="text-center">
    <h1 class="text-f45 text-france-blue">Proposez un service</h1>
    <div class="paragraph-small mt-s16">
      Aidez-nous à identifier et référencer l’ensemble de l’offre de
      l’insertion.<br />
      Seuls les champs marqués d’un astérisque<span
        style="color: var(--col-error);">*</span
      > sont obligatoires.
    </div>
  </div>
</CenteredGrid>

<FormErrors />

<CenteredGrid bgColor="bg-gray-bg">
  <div class="lg:w-2/3">
    <Form
      data={service}
      schema={contribSchema}
      onChange={handleChange}
      onSubmit={handleSubmit}
      onSuccess={handleSuccess}
      bind:requesting
    >
      <Fields bind:service servicesOptions={data.servicesOptions} />

      {#if service.siret}
        <div class="mt-s32 flex flex-col justify-end md:flex-row ">
          <Button
            name="validate"
            type="submit"
            label="Envoyer la contribution"
            disabled={requesting}
          />
        </div>
      {/if}
    </Form>
  </div>
</CenteredGrid>
