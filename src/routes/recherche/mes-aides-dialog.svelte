<script lang="ts">
  import Dialog from "$lib/components/hoc/dialog.svelte";
</script>

<Dialog isOpen={true}>
  <a
    href="https://mes-aides.francetravail.fr/?at_medium=custom1&at_campaign=MA&at_custom1=Dora&at_custom2=HP&at_custom3=Mobilite0924"
    target="_blank"
    id="mtm-bloc-mes-aides"
  >
    <div class="py-s12">
      <span class="rounded-lg bg-magenta-20 px-s8 text-france-blue"
        >Vous êtes un particulier ?</span
      >
      <h3 class="my-s9 text-france-blue">
        Trouvez vos aides locales avec Mes Aides
      </h3>
      <p class="m-s0">
        Le service public numérique gratuit où trouver toutes les aides
        financières, matérielles et pédagogiques pour chercher, trouver et
        conserver un emploi.
      </p>
    </div>
  </a>
</Dialog>
