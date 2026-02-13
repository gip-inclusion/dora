<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import { userInfo } from "$lib/utils/auth";
  import { EMPLOIS_PORTAL_PAGE_URL } from "$lib/env";

  import { ALL_SERVICES } from "./consts";
  import MenuMonPortailServiceItem from "./menu-mon-portail-service-item.svelte";
  import type { NexusServiceID, NexusDropDownStatus } from "./types";

  interface Props {
    mobileDesign?: boolean;
  }

  let { mobileDesign = false }: Props = $props();

  export const ACTIVABLE_SERVICES: NexusServiceID[] = [
    "les-emplois",
    "dora",
    "pilotage",
  ];

  export const NEXUS_DROP_DOWN_STATUS: NexusDropDownStatus = {
    proconnect: true,
    // eslint-disable-next-line camelcase
    activated_services: ["dora", "les-emplois"],
    "mvp-enabled": true,
  };

  const enabledServices = ALL_SERVICES.filter((service) =>
    NEXUS_DROP_DOWN_STATUS.activated_services.includes(service.id)
  );
  const disabledServices = ALL_SERVICES.filter(
    (service) => !NEXUS_DROP_DOWN_STATUS.activated_services.includes(service.id)
  );
</script>

<DropdownMenu labelText="Mon portail" withBorders {mobileDesign}>
  <div class="flex flex-col">
    <p class="text-f14 text-gray-text leading-24">
      <strong>{$userInfo?.firstName} {$userInfo?.lastName}</strong><br
      />{$userInfo?.email}
    </p>

    <LinkButton
      to={EMPLOIS_PORTAL_PAGE_URL}
      otherTab
      nofollow
      secondary
      wFull
      extraClass="mb-s16"
      label="Accéder à mon portail"
    />

    {#each enabledServices as service}
      <MenuMonPortailServiceItem {service} activated />
    {/each}

    <hr />

    {#each disabledServices as service}
      <MenuMonPortailServiceItem
        {service}
        activable={ACTIVABLE_SERVICES.includes(service.id)}
      />
    {/each}
  </div>
</DropdownMenu>
