<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import StickyFormSubmissionRow from "$lib/components/forms/sticky-form-submission-row.svelte";
  import ContactBox from "./contact-box.svelte";
  import Layout from "./orientation-layout.svelte";
  import ValidationForm from "./validation-form.svelte";
  import { orientation } from "./store";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import { orientationStep1Schema } from "./schema";
  import { goto } from "$app/navigation";
  import { arrowLeftLineIcon } from "$lib/icons";
  import { onMount } from "svelte";

  export let data;

  const { service } = data;

  let requesting = false;

  onMount(() => {
    $orientation.firstStepDone = true;
  });

  function handleChange(validatedData) {
    $orientation = { ...validatedData };
  }

  function handleSubmit(_validatedData) {
    // Pas de soumission au backend à cette étape
    return { ok: true };
  }

  function handleSuccess(_result) {
    goto(`/services/${service.slug}/orienter/demande`);
  }
</script>

<FormErrors />

<Form
  bind:data={$orientation}
  schema={orientationStep1Schema}
  disableExitWarning
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  <Layout {data}>
    <p class="legend">Étape 1 sur 2</p>
    <h2 class="mb-s0">Valider la conformité</h2>
    <p class="legend">
      <strong>Étape suivante</strong>&nbsp;: Compléter la demande
    </p>
    <hr class="my-s40" />
    <p class="mb-s40 max-w-2xl text-f18">
      Avant de commencer la procédure, vérifiez l’éligibilité du ou de la
      bénéficiaire et consultez la liste des documents requis.
    </p>

    <div class="flex flex-col justify-between gap-x-s24 md:flex-row">
      <ValidationForm {service} />
      <div class="mt-s32 w-full shrink-0 md:mt-s0 md:w-[384px]">
        <ContactBox {service} />
      </div>
    </div>
  </Layout>

  <StickyFormSubmissionRow justifyBetween>
    <LinkButton
      icon={arrowLeftLineIcon}
      to="/services/{service.slug}"
      label="Retour à la fiche"
      secondary
    />

    <Button id="publish" type="submit" label="Étape suivante" />
  </StickyFormSubmissionRow>
</Form>
