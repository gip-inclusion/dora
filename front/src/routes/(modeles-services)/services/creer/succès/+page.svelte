<script lang="ts">
  import illustration from "$lib/assets/illustrations/Referencer_Vos_Services.webp";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
</script>

<CenteredGrid>
  <h1 class="mb-s40">Service créé avec succès</h1>
  <div
    class="border-gray-02 py-s32 px-s20 gap-s40 flex flex-col items-center rounded-2xl border text-center md:flex-row"
  >
    <div>
      <h2>Votre service est publié et sera bientôt visible partout</h2>
      <p class="text-f14">
        Dans un délai maximum d'une heure votre service sera accessible dans les
        résultats de recherche de DORA - ainsi que sur les autres plateformes
        partenaires via le référentiel commun numérique data·inclusion.
      </p>
      <p class="text-f14">
        Ce court délai est nécessaire pour que les informations transitent par
        le référentiel commun data·inclusion qui centralise toutes les données
        de l'offre d'insertion.
      </p>
    </div>
    <div class="w-full max-w-[443px]">
      <img src={illustration} alt="" aria-hidden="true" />
    </div>
  </div>
</CenteredGrid>
