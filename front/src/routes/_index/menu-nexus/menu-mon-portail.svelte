<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import { userInfo } from "$lib/utils/auth";
  import { EMPLOIS_PORTAL_PAGE_URL } from "$lib/env";

  import { ALL_SERVICES } from "./consts";
  import MenuMonPortailServiceItem from "./menu-mon-portail-service-item.svelte";
  import type { NexusServiceID } from "$lib/requests/nexus";
  import type { NexusDropDownStatus } from "$lib/requests/nexus";

  const ACTIVABLE_SERVICES: NexusServiceID[] = [
    "les-emplois",
    "dora",
    "pilotage",
  ];

  interface Props {
    dropdownStatus: NexusDropDownStatus;
    mobileDesign?: boolean;
  }

  let { dropdownStatus, mobileDesign = false }: Props = $props();

  let enabledServices = $derived(
    ALL_SERVICES.filter((service) =>
      dropdownStatus.activatedServices.includes(service.id)
    )
  );
  let disabledServices = $derived(
    ALL_SERVICES.filter(
      (service) => !dropdownStatus.activatedServices.includes(service.id)
    )
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
