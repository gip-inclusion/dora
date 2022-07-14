<script>
  import StructureSearch from "$lib/components/structures/search.svelte";
  import { registrationInfo } from "./_store.js";

  export let currentStep;
  export let siret = "";

  let establishment;
  let tabId;

  function handleJoin() {
    plausible("inscription", { props: { step: "Création structure" } });
    $registrationInfo.siret = establishment.siret;
    $registrationInfo.isPoleEmploi = tabId === "safir";
    currentStep = 2;
  }
</script>

<StructureSearch
  hasSafir
  hasValidation
  onValidate={handleJoin}
  {siret}
  bind:establishment
  bind:tabId
/>
