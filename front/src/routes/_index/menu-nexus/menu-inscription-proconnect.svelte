<script lang="ts">
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  import { page } from "$app/state";

  import logoNexus from "$lib/assets/logos/logo-nexus.png";
  import logoNexusDropdownIcon from "$lib/assets/logos/logo-nexus-dropdown.svg";

  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import PcButton from "$lib/components/specialized/pc-button.svelte";

  import { PROCONNECT_MORE_INFO_URL } from "$lib/consts";

  import { getNextPage } from "../../auth/utils";

  interface Props {
    mobileDesign?: boolean;
  }

  let { mobileDesign = false }: Props = $props();

  const nextPage = getNextPage(page.url);
</script>

<DropdownMenu withBorders withSeparator={false} {mobileDesign}>
  {#snippet label()}
    <span class="gap-s10 text-magenta-cta flex items-center font-bold">
      <img
        src={logoNexusDropdownIcon}
        class="h-s24 w-s24"
        alt="Logo Nexus"
        aria-hidden="true"
      />
      Mon portail
    </span>
  {/snippet}
  <div class="py-s4 px-s12 flex flex-col items-center lg:w-[303px]">
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
      Pour accéder à votre portail, vous devez avoir un compte ProConnect.
    </p>

    <div class="mb-s16">
      <PcButton {nextPage} noHelpSection />
    </div>

    <LinkButton
      label="En savoir plus"
      to={PROCONNECT_MORE_INFO_URL}
      small
      otherTab
      nofollow
      noBackground
      icon={ExternalLinkLineSystem}
      iconOnRight
    />
  </div>
</DropdownMenu>
