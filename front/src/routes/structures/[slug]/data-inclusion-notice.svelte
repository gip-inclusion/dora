<script lang="ts">
  import orphanStructuresImg from "$lib/assets/illustrations/illu-structures-orphelines.svg";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import type { Structure } from "$lib/types";

  interface Props {
    structure: Structure;
  }

  let { structure }: Props = $props();

  let sourceName = $derived(structure.source?.label);
</script>

<div
  class="mt-s40 gap-s16 bg-info-light px-s24 py-s40 md:gap-s112 md:px-s112 flex flex-col rounded-3xl md:flex-row"
>
  <div class="grow self-center md:shrink-0">
    <img
      src={orphanStructuresImg}
      alt=""
      class="h-[120px] w-[126px] md:h-[227px] md:w-[238px]"
    />
  </div>
  <div>
    <h3>
      Des informations de votre structure provenant de «&nbsp;{sourceName}&nbsp;»
      sont déjà préremplies pour vous sur DORA&nbsp;!
    </h3>
    <p class="legende mb-s40 text-f14">
      Dora s’associe à <strong
        >Data Inclusion, le référentiel partagé des offres d’insertion</strong
      >. Avec cette démarche de
      <strong>«&nbsp;Dites-le-nous une fois&nbsp;»</strong>, certaines
      informations de votre structure présentes sur «&nbsp;{sourceName}&nbsp;»
      se retrouvent sur DORA. Vous pouvez les conserver à l’identique ou les
      modifier selon vos besoins.
    </p>
    <LinkButton
      label="Compléter vos informations"
      to="/structures/{structure.slug}/editer"
    />
  </div>
</div>
