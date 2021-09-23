<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import connexionPic from "$lib/assets/illu_connexion-optimise.svg";

  import StepTypology from "./registration/_step1-typology.svelte";

  import StepPoleEmploi from "./registration/_step2-pe.svelte";
  import StepOther from "./registration/_step3-other.svelte";
  import StepUser from "./registration/_step4-user.svelte";
  import StepConfirm from "./registration/_step5-confirm.svelte";

  const steps = new Map([
    [1, StepTypology],
    [2, StepPoleEmploi],
    [3, StepOther],
    [4, StepUser],
    [5, StepConfirm],
  ]);

  let currentStep = 1;

  $: currentStepComponent = steps.get(currentStep);
</script>

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Créer son compte DORA</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="col-start-1 col-end-7 mb-4 mt-6">
    <img src={connexionPic} alt="" />
  </div>
  <div class="col-start-7 col-end-13 mb-4">
    <svelte:component this={currentStepComponent} bind:currentStep />
  </div>
</CenteredGrid>
