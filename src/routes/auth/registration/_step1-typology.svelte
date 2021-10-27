<script>
  import ButtonDetails from "$lib/components/button-details.svelte";
  import Fieldset from "$lib/components/forms/fieldset.svelte";

  export let currentStep;
</script>

<Fieldset
  title="Votre structure"
  description="Chaque utilisateur DORA est attaché à une structure d’insertion (de l’Etat ou associative/independante. Afin de mieux vous aider à identifier votre structure, merci de choisir la typologie de votre structure :"
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
