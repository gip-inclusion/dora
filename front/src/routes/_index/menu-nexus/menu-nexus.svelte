<script lang="ts">
  import { onMount } from "svelte";

  import logoNexusDropdownIcon from "$lib/assets/logos/logo-nexus-dropdown.svg";

  import {
    getNexusDropdownStatus,
    type NexusDropDownStatus,
  } from "$lib/requests/nexus";

  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import MenuInscriptionEmplois from "./menu-inscription-emplois.svelte";
  import MenuInscriptionProconnect from "./menu-inscription-proconnect.svelte";
  import MenuMonPortail from "./menu-mon-portail.svelte";

  interface Props {
    mobileDesign?: boolean;
  }

  let { mobileDesign = false }: Props = $props();

  let dropdownStatus: NexusDropDownStatus | undefined = $state(undefined);

  onMount(() => {
    getNexusDropdownStatus().then((status) => {
      dropdownStatus = status;
    });
  });
</script>

{#if dropdownStatus && dropdownStatus.mvpEnabled}
  <DropdownMenu withBorders withSeparator={false} {mobileDesign}>
    {#snippet label()}
      <span class="gap-s10 text-magenta-cta flex items-center font-bold">
        <img
          src={logoNexusDropdownIcon}
          class="h-s24 w-s24"
          alt=""
          aria-hidden="true"
        />
        Mon portail
      </span>
    {/snippet}
    {#if !dropdownStatus.activatedServices.includes("les-emplois")}
      <MenuInscriptionEmplois />
    {:else if !dropdownStatus.proconnect}
      <MenuInscriptionProconnect />
    {:else}
      <MenuMonPortail {dropdownStatus} />
    {/if}
  </DropdownMenu>
{/if}
