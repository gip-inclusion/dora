<script lang="ts">
  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";
  import { page } from "$app/stores";
  import { token, userInfo } from "$lib/utils/auth";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { capitalize } from "$lib/utils/misc";
  import MembershipPendingWarning from "$lib/components/specialized/membership-pending-warning.svelte";
  import Notice from "$lib/components/display/notice.svelte";

  export let data;

  const { service } = data;

  $: isDI = "source" in service;

  let currentLocation = $token
    ? "service-orientation-step1"
    : "service-orientation";
  if ($page.url.pathname.endsWith("/orienter/demande")) {
    currentLocation = "service-orientation-step2";
  } else if ($page.url.pathname.endsWith("/orienter/merci")) {
    currentLocation = "service-orientation-confirmation";
  }
</script>

<CenteredGrid bgColor="bg-service-blue-light">
  <Breadcrumb {service} structure={service.structureInfo} {currentLocation} />
  <div class="gap-s6 text-f14 mt-s24 mb-s16 text-gray-text flex items-center">
    <HomeSmileLineBuildings size="16" />
    <strong>
      {#if !isDI}
        <a href="/structures/{service.structureInfo.slug}" class="underline"
          >{capitalize(service.structureInfo.name)}</a
        >
      {:else}
        {capitalize(service.structureInfo.name)}
      {/if}
    </strong>
  </div>
  <h1 class="mb-s0 mr-s12 text-magenta-dark">
    <span class="text-f38 leading-s48">Formulaire d’orientation&#8239;:</span>
    <span class="mt-s2 text-f28 leading-s40 block">{service.name}</span>
  </h1>
</CenteredGrid>

<CenteredGrid bgColor="bg-white" roundedColor="bg-service-blue-light">
  {#if $userInfo && !$userInfo.structures.length}
    <div class="m-auto max-w-xl">
      <Notice type="warning">
        <MembershipPendingWarning />
      </Notice>
    </div>
  {:else}
    <slot />
  {/if}
</CenteredGrid>

<slot name="navbar" />
