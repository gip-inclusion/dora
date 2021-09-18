<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import connexionPic from "$lib/assets/illu_connexion-optimise.svg";

  import StepTypology from "./registration/_step1-typology.svelte";
  import StepPE1 from "./registration/_step2-pe1.svelte";
  import StepPE2 from "./registration/_step3-pe2.svelte";
  import StepOther1 from "./registration/_step4-other1.svelte";
  import StepOther2 from "./registration/_step5-other2.svelte";
  import StepUser from "./registration/_step6-user.svelte";
  import StepConfirm from "./registration/_step7-confirm.svelte";

  const steps = new Map([
    [1, StepTypology],
    [2, StepPE1],
    [3, StepPE2],
    [4, StepOther1],
    [5, StepOther2],
    [6, StepUser],
    [7, StepConfirm],
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
