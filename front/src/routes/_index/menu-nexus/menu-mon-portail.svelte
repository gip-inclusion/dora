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

  let enabledServices = $derived(
    ALL_SERVICES.filter((service) =>
      nexusMenuStatus.activatedServices.includes(service.id)
    )
  );
  let disabledServices = $derived(
    ALL_SERVICES.filter(
      (service) => !nexusMenuStatus.activatedServices.includes(service.id)
    )
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

  {#each enabledServices as service}
    <MenuMonPortailServiceItem {service} activated />
  {/each}

  <hr />

  {#each disabledServices as service}
    <MenuMonPortailServiceItem
      {service}
      activableInOneClick={ACTIVABLE_IN_ONE_CLICK_SERVICES.includes(service.id)}
    />
  {/each}
</div>
