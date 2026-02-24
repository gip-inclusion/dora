<script lang="ts">
  import { onMount } from "svelte";

  import logoNexusMenuIcon from "$lib/assets/logos/logo-nexus-menu.svg";

  import {
    getNexusMenuStatus,
    type NexusMenuStatus,
  } from "$lib/requests/nexus";

  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import MenuInscriptionEmplois from "./menu-inscription-emplois.svelte";
  import MenuInscriptionProconnect from "./menu-inscription-proconnect.svelte";
  import MenuMonPortail from "./menu-mon-portail.svelte";

  interface Props {
    mobileDesign?: boolean;
  }

  let { mobileDesign = false }: Props = $props();

  let nexusMenuStatus: NexusMenuStatus | undefined = $state(undefined);

  onMount(() => {
    getNexusMenuStatus().then((status) => {
      nexusMenuStatus = status;
    });
  });
</script>

{#if nexusMenuStatus && nexusMenuStatus.enabled}
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
