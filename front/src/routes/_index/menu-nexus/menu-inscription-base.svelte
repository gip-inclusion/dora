<script lang="ts">
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  import logoNexus from "$lib/assets/logos/logo-nexus.png";

  import LinkButton from "$lib/components/display/link-button.svelte";

  import { EMPLOIS_MORE_INFO_URL } from "$lib/consts";

  import type { Snippet } from "svelte";

  interface Props {
    text: string;
    children: Snippet;
  }

  let { text, children }: Props = $props();
</script>

<div class="py-s4 px-s12 flex flex-col items-center lg:w-[327px]">
  <div class="my-s8 flex items-center justify-center">
    <img src={logoNexus} alt="Plateforme de l’inclusion" class="w-[197px]" />
  </div>

  <h4 class="mb-s16 text-f18 text-france-blue leading-24 font-bold">
    Découvrez votre nouveau portail unifié&#8239;!
  </h4>

  <p class="mb-s16 text-f14 text-gray-text leading-24">
    Accédez bientôt à l’ensemble de votre offre et de vos informations.
  </p>

  <hr class="mb-s16 border-gray-01 w-full" />

  <p class="mb-s16 text-f14 text-gray-text leading-24">
    {text}
  </p>

  {@render children()}

  <LinkButton
    label="En savoir plus"
    to={EMPLOIS_MORE_INFO_URL}
    small
    otherTab
    nofollow
    noBackground
    icon={ExternalLinkLineSystem}
    iconOnRight
  />
</div>
