<script lang="ts">
  import { onMount } from "svelte";
  import {
    getNexusDropdownStatus,
    type NexusDropDownStatus,
  } from "$lib/requests/nexus";
  import MenuMonPortail from "./menu-mon-portail.svelte";
  import MenuInscriptionEmplois from "./menu-inscription-emplois.svelte";
  import MenuInscriptionProconnect from "./menu-inscription-proconnect.svelte";

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
  {#if !dropdownStatus.activatedServices.includes("les-emplois")}
    <MenuInscriptionEmplois {mobileDesign} />
  {:else if !dropdownStatus.proconnect}
    <MenuInscriptionProconnect {mobileDesign} />
  {:else}
    <MenuMonPortail {dropdownStatus} {mobileDesign} />
  {/if}
{/if}
