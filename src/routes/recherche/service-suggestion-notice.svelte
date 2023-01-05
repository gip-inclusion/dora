<script lang="ts">
  import illuSuggerer from "$lib/assets/illustrations/illu-suggerer.svg";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import EmailButton from "$lib/components/specialized/email-button.svelte";
</script>

<div class="flex rounded-md border border-gray-01 bg-white shadow-md">
  <div
    class="hidden flex-[1] items-center justify-center bg-service-violet md:flex"
  >
    <img src={illuSuggerer} alt="" />
  </div>

  <div class="flex-[1] p-s32">
    <h2 class="text-f17 font-bold leading-28 text-gray-text">
      Demain vos partenaires locaux seront ici… aidez-nous à les identifier 😊
    </h2>
    <p class="mb-s32 text-f14">
      En tant qu’experts, vous avez une connaissance étendue de l’offre
      d’insertion de votre territoire. Participez à notre démarche collective en
      suggérant les services de vos partenaires locaux.
    </p>
    <div class="flex flex-col gap-s16">
      <LinkButton label="Suggérer un service" wFull to="/contribuer" />
      <EmailButton wFull />
    </div>
  </div>
</div>
