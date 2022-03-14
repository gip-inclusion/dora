<script>
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import StepStructureSearch from "./registration/_step1-structure-search.svelte";
  import StepUser from "./registration/_step2-user.svelte";
  import StepConfirm from "./registration/_step3-confirm.svelte";
  import AuthLayout from "./_auth_layout.svelte";

  const siret = $page.url.searchParams.get("siret");

  const steps = new Map([
    [1, StepStructureSearch],
    [2, StepUser],
    [3, StepConfirm],
  ]);

  let currentStep = 1;

  $: currentStepComponent = steps.get(currentStep);
</script>

<svelte:head>
  <title>Créer son compte | DORA</title>
</svelte:head>

<CenteredGrid topPadded>
  <div class="col-span-full col-start-1 mb-s48 text-center">
    <h1 class="text-france-blue">Création de compte</h1>
  </div>
</CenteredGrid>

<AuthLayout wideForm>
  <svelte:component this={currentStepComponent} bind:currentStep {siret} />
</AuthLayout>
