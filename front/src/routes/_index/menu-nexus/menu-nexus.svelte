<script lang="ts">
  import logoNexusMenuIcon from "$lib/assets/logos/logo-nexus-menu.svg";
  import type { NexusMenuStatus } from "$lib/requests/nexus";
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import MenuInscriptionEmplois from "./menu-inscription-emplois.svelte";
  import MenuInscriptionProconnect from "./menu-inscription-proconnect.svelte";
  import MenuMonPortail from "./menu-mon-portail.svelte";

  interface Props {
    nexusMenuStatus: NexusMenuStatus | undefined;
    mobileDesign?: boolean;
  }

  let { nexusMenuStatus, mobileDesign = false }: Props = $props();
</script>

{#if nexusMenuStatus && nexusMenuStatus.mvpEnabled}
  <DropdownMenu withBorders withSeparator={false} {mobileDesign}>
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
    {#if !nexusMenuStatus.activatedServices.includes("les-emplois")}
      <MenuInscriptionEmplois />
    {:else if !nexusMenuStatus.proconnect}
      <MenuInscriptionProconnect />
    {:else}
      <MenuMonPortail {nexusMenuStatus} />
    {/if}
  </DropdownMenu>
{/if}
