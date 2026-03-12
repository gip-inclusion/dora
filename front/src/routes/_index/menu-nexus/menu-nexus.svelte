<script lang="ts">
  import logoNexusMenuIcon from "$lib/assets/logos/logo-plateforme-inclusion-mono.svg";
  import type { NexusMenuStatus } from "$lib/requests/nexus";
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";
  import { trackMatomoEvent } from "$lib/utils/matomo";

  import MenuInscriptionEmplois from "./menu-inscription-emplois.svelte";
  import MenuInscriptionProconnect from "./menu-inscription-proconnect.svelte";
  import MenuMonPortail from "./menu-mon-portail.svelte";

  interface Props {
    nexusMenuStatus: NexusMenuStatus | undefined;
    mobileDesign?: boolean;
  }

  type Menu = "inscription-emplois" | "inscription-proconnect" | "mon-portail";

  let { nexusMenuStatus, mobileDesign = false }: Props = $props();

  function getCurrentMenu(status: NexusMenuStatus | undefined): Menu | null {
    if (!status) {
      return null;
    }

    if (!status.activatedServices.includes("les-emplois")) {
      return "inscription-emplois";
    }

    if (!status.proconnect) {
      return "inscription-proconnect";
    }

    return "mon-portail";
  }

  let currentMenu = $derived(getCurrentMenu(nexusMenuStatus));

  function handleClick(isOpen: boolean) {
    if (isOpen && currentMenu === "mon-portail") {
      trackMatomoEvent({
        category: "Nexus",
        action: "mon-portail",
      });
    }
  }
</script>

{#if nexusMenuStatus && nexusMenuStatus.mvpEnabled}
  <DropdownMenu
    withBorders
    withSeparator={false}
    {mobileDesign}
    onclick={handleClick}
  >
    {#snippet label()}
      <span class="gap-s10 text-magenta-cta flex items-center font-bold">
        <img
          src={logoNexusMenuIcon}
          class="h-s24 w-s24"
          alt=""
          aria-hidden="true"
        />
        Mon portail
      </span>
    {/snippet}
    {#if currentMenu === "inscription-emplois"}
      <MenuInscriptionEmplois />
    {:else if currentMenu === "inscription-proconnect"}
      <MenuInscriptionProconnect />
    {:else if currentMenu === "mon-portail"}
      <MenuMonPortail {nexusMenuStatus} />
    {/if}
  </DropdownMenu>
{/if}
