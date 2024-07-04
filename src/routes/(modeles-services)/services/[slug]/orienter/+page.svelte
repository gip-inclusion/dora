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
  import { onMount, setContext } from "svelte";
  import { token } from "$lib/utils/auth";
  import Teaser from "./teaser.svelte";
  import { trackMobilisation } from "$lib/utils/stats";
  import { page } from "$app/stores";
  export let data;

  const { service } = data;
  const isDI = !!data.isDI;

  let requesting = false;

  // tracking activé sur la page courante :
  const shouldTrack = Boolean($page.url.searchParams.get("newlogin"));

  // On ne doit pas tracker la mobilisation sur affichage de contacts
  // (ou toute autre action)
  // si on se trouve sur la page du formulaire d'orientation :
  // la mobilisation est déjà comptabilisé à l'ouverture du formulaire.
  // On doit transmettre cette information de manière générique
  // au composant enfant 'ContactInfo'.

  // Raccourci : on ne peut accéder à cette page que si connecté.
  setContext("shouldTrack", !$token);

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
    goto(`/services/${isDI ? "di--" : ""}${service.slug}/orienter/demande`);
  }

  onMount(async () => {
    if ($token && shouldTrack) {
      await trackMobilisation(service, $page.url, isDI);
      $page.url.searchParams.delete("newlogin");
      history.replaceState(null, "", $page.url.pathname + $page.url.search);
    }
  });
</script>

{#if $token}
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
          <ContactBox {service} {isDI} />
        </div>
      </div>
    </Layout>
    <StickyFormSubmissionRow justifyBetween>
      <LinkButton
        icon={arrowLeftLineIcon}
        to="/services/{isDI ? 'di--' : ''}{service.slug}"
        label="Retour à la fiche"
        secondary
      />

      <Button id="publish" type="submit" label="Étape suivante" />
    </StickyFormSubmissionRow>
  </Form>
{:else}
  <Layout {data}>
    <Teaser {service} {isDI}></Teaser>
  </Layout>
{/if}
