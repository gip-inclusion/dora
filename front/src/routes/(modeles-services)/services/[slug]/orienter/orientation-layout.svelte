<script lang="ts">
  import { page } from "$app/stores";
  import { token, userInfo } from "$lib/utils/auth";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { capitalize } from "$lib/utils/misc";
  import MembershipPendingWarning from "$lib/components/specialized/membership-pending-warning.svelte";
  import Notice from "$lib/components/display/notice.svelte";

  let { data, children, navbar } = $props();

  const { service } = data;

  let currentLocation = $state($token
    ? "service-orientation-step1"
    : "service-orientation");
  if ($page.url.pathname.endsWith("/orienter/demande")) {
    currentLocation = "service-orientation-step2";
  } else if ($page.url.pathname.endsWith("/orienter/merci")) {
    currentLocation = "service-orientation-confirmation";
  }
</script>

<CenteredGrid bgColor="bg-france-blue">
  <div class="mb-s48 print:mb-s0">
    <Breadcrumb {service} structure={service.structureInfo} {currentLocation} />
  </div>
  <h1 class="print:text-france-blue text-white">
    Orienter un ou une bénéficiaire vers le service&nbsp;:
  </h1>
  <h2 class="print:text-france-blue text-white">
    {service.name}
  </h2>
  <h3 class=" print:text-france-blue text-white">
    <div><strong>{capitalize(service.structureInfo.name)}</strong></div>
  </h3>
</CenteredGrid>

<CenteredGrid bgColor="bg-white" roundedColor="bg-france-blue">
  {#if $userInfo && !$userInfo.structures.length}
    <div class="m-auto max-w-xl">
      <Notice type="warning">
        <MembershipPendingWarning />
      </Notice>
    </div>
  {:else}
    {@render children?.()}
  {/if}
</CenteredGrid>

{@render navbar?.()}
