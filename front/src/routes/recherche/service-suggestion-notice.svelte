<script lang="ts">
  import illuSuggerer from "$lib/assets/illustrations/illu-suggerer.svg";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import InviteStructureLink from "$lib/components/specialized/invite-structure-link.svelte";
</script>

<div class="border-gray-01 flex rounded-lg border bg-white shadow-md">
  <div
    class="bg-service-violet hidden flex-1 items-center justify-center md:flex"
  >
    <img src={illuSuggerer} alt="" />
  </div>

  <div class="p-s32 flex-1">
    <h2 class="text-f17 text-gray-text leading-28 font-bold">
      Demain vos partenaires locaux seront ici… aidez-nous à les identifier 😊
    </h2>
    <p class="mb-s32 text-f14">
      En tant qu’experts, vous avez une connaissance étendue de l’offre
      d’insertion de votre territoire. Participez à notre démarche collective en
      suggérant les services de vos partenaires locaux.
    </p>
    <div class="gap-s16 flex flex-col">
      <LinkButton label="Suggérer un service" wFull to="/contribuer" />
      <InviteStructureLink wFull />
    </div>
  </div>
</div>
