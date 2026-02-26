<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";

  import { userInfo } from "$lib/utils/auth";

  import { EMPLOIS_PORTAL_PAGE_URL } from "$lib/env";

  import type { NexusServiceID } from "$lib/requests/nexus";
  import type { NexusMenuStatus } from "$lib/requests/nexus";

  import { trackMatomoEvent } from "$lib/utils/matomo";

  import { ALL_SERVICES } from "./consts";

  import MenuMonPortailServiceItem from "./menu-mon-portail-service-item.svelte";

  const ACTIVABLE_IN_ONE_CLICK_SERVICES: NexusServiceID[] = [
    "les-emplois",
    "dora",
    "pilotage",
  ];

  interface Props {
    nexusMenuStatus: NexusMenuStatus;
  }

  let { nexusMenuStatus }: Props = $props();

  let activatedServices = $derived(
    ALL_SERVICES.filter((service) =>
      nexusMenuStatus.activatedServices.includes(service.id)
    )
  );
  let deactivatedServices = $derived(
    ALL_SERVICES.filter(
      (service) => !nexusMenuStatus.activatedServices.includes(service.id)
    )
  );
  let showSeparator = $derived(
    activatedServices.length > 0 && deactivatedServices.length > 0
  );

  function handleClick() {
    trackMatomoEvent({
      category: "Nexus",
      action: "acceder-mon-portail",
      name: "dora",
    });
  }
</script>

<div class="flex flex-col lg:w-[344px]">
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
    onclick={handleClick}
  />

  {#each activatedServices as service}
    <MenuMonPortailServiceItem {service} activated />
  {/each}

  {#if showSeparator}
    <hr />
  {/if}

  {#each deactivatedServices as service}
    <MenuMonPortailServiceItem
      {service}
      activableInOneClick={ACTIVABLE_IN_ONE_CLICK_SERVICES.includes(service.id)}
    />
  {/each}
</div>
