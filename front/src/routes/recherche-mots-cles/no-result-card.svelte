<script lang="ts">
  import illustration from "$lib/assets/illustrations/illu-structures-orphelines.svg";
  import LinkButton from "$lib/components/display/link-button.svelte";
</script>

<div
  class="border-gray-02 flex flex-col overflow-hidden rounded-2xl border shadow-sm lg:flex-row"
>
  <div class="bg-magenta-10 p-s32 flex items-center justify-center lg:w-2/5">
    <img src={illustration} alt="" class="max-w-full" />
  </div>

  <div class="p-s32 lg:w-3/5">
    <h3 class="text-france-blue text-f24 font-bold">
      Des services correspondants à votre recherche sont absents des
      résultats&nbsp;?
    </h3>
    <p class="mt-s16 text-f16 text-gray-text">
      Il se peut que les structures près de chez vous n’aient pas encore
      référencé leurs services sur DORA. Participez à notre démarche collective
      en identifiant vos partenaires locaux&nbsp;!
    </p>
    <div class="mt-s24 gap-s12 flex flex-col">
      <LinkButton to="/services/creer" label="Proposer un service" wFull />
      <LinkButton
        to="https://tally.so/r/nGegBe"
        otherTab
        secondary
        label="Inviter un porteur de service"
        wFull
      />
    </div>
  </div>
</div>
