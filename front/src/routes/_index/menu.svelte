<script lang="ts">
  import { onMount } from "svelte";

  import { page } from "$app/stores";

  import HamburgerMenu from "$lib/components/display/hamburger.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import {
    getNexusMenuStatus,
    type NexusMenuStatus,
  } from "$lib/requests/nexus";
  import type { ShortStructure } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";
  import { userPreferences } from "$lib/utils/preferences";

  import MenuAide from "./menu-aide.svelte";
  import MenuMesStructures from "./menu-mes-structures.svelte";
  import MenuMonCompte from "./menu-mon-compte.svelte";
  import MenuNexus from "./menu-nexus/menu-nexus.svelte";
  import SubMenu from "./sub-menu.svelte";

  let nexusMenuStatus = $state<NexusMenuStatus | undefined>(undefined);

  onMount(() => {
    getNexusMenuStatus().then((status) => {
      nexusMenuStatus = status;
    });
  });

  let structures: ShortStructure[] = $derived(
    $userInfo ? [...$userInfo.structures, ...$userInfo.pendingStructures] : []
  );
  let lastVisitedStructure: ShortStructure | undefined = $derived(
    getCurrentlySelectedStructure($userInfo, $userPreferences)
  );
</script>

<HamburgerMenu>
  <div class="flex flex-col lg:flex-row print:hidden">
    <div class="mb-s16 lg:mb-s0 lg:mr-s16 h-[50px]">
      <MenuAide />
    </div>

    {#if !$userInfo}
      {#if $page.url.pathname !== "/auth/connexion"}
        <LinkButton
          label="Se connecter"
          to={`/auth/connexion?next=${encodeURIComponent(
            $page.url.pathname + $page.url.search
          )}`}
        />
      {/if}
    {:else}
      <div class="gap-s10 hidden lg:flex">
        <MenuMesStructures {structures} {lastVisitedStructure} />
        <MenuMonCompte />
        <MenuNexus {nexusMenuStatus} />
      </div>
    {/if}

    <div class="gap-s10 flex flex-col lg:hidden">
      {#if $userInfo}
        <MenuMesStructures {structures} {lastVisitedStructure} mobileDesign />
        <MenuMonCompte mobileDesign />
        <MenuNexus {nexusMenuStatus} mobileDesign />
      {/if}
      <hr class="-mx-s32 mb-s16 mt-s64" />
      <SubMenu mobileDesign />
    </div>
  </div>
</HamburgerMenu>
