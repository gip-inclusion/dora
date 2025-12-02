<script lang="ts">
  import type { Snippet } from "svelte";
  import { page } from "$app/stores";
  import { getToken, userInfo } from "$lib/utils/auth";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import MembershipPendingWarning from "$lib/components/specialized/membership-pending-warning.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import ServiceStructureLabel from "../components/service-structure-label.svelte";
  import type { Service } from "$lib/types";

  interface Props {
    data: { service: Service };
    children?: Snippet;
    navbar?: Snippet;
  }

  let { data, children, navbar }: Props = $props();

  const { service } = data;

  let currentLocation = $state(
    getToken() ? "service-orientation-step1" : "service-orientation"
  );
  if ($page.url.pathname.endsWith("/orienter/demande")) {
    currentLocation = "service-orientation-step2";
  } else if ($page.url.pathname.endsWith("/orienter/merci")) {
    currentLocation = "service-orientation-confirmation";
  }
</script>

<CenteredGrid bgColor="bg-blue-light">
  <Breadcrumb {service} structure={service.structureInfo} {currentLocation} />
  <div class="mt-s48 mb-s16"><ServiceStructureLabel {service} /></div>
  <h1 class="mb-s0 mr-s12 text-magenta-dark">
    <span class="text-f38 leading-s48">Formulaire d’orientation&#8239;:</span>
    <span class="mt-s2 text-f28 leading-s40 block">{service.name}</span>
  </h1>
</CenteredGrid>

<CenteredGrid roundedColor="bg-blue-light">
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
