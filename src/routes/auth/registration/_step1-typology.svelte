<script>
  import ButtonDetails from "$lib/components/button-details.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";

  export let currentStep;
</script>

<Fieldset
  title="Votre structure"
  description="Sur Dora, chaque utilisateur est rattaché à une structure, cette étape nous permet de faciliter votre inscription. Si vous êtes agent Pôle emploi, cliquez sur l’option correspondante. Sinon, cliquez sur l'option “Autre structure”."
>
  <ButtonDetails
    label="Pôle Emploi"
    details="Vous êtes un agent d’Etat rattaché à une agence Pôle emploi"
    on:click={() => (currentStep = 2)}
  />
  <ButtonDetails
    label="Autre type de structures"
    details="Vous êtes salarié, bénévole, agent d'Etat rattaché à une structure d'insertion."
    on:click={() => (currentStep = 3)}
  />
</Fieldset>
