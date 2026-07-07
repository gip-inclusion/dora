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
      Aucun service pertinent&nbsp;?
    </h3>
    <p class="mt-s16 text-f16 text-gray-text">
      Il se peut que les structures n’aient pas encore référencé leur offre sur
      DORA, vous pouvez y remédier&nbsp;:
    </p>
    <div class="mt-s24 gap-s12 flex flex-col">
      <LinkButton to="/services/creer" label="Référencer un service" wFull />
      <LinkButton
        to="https://tally.so/r/nGegBe"
        otherTab
        secondary
        label="Inviter une structure"
        wFull
      />
    </div>
  </div>
</div>
