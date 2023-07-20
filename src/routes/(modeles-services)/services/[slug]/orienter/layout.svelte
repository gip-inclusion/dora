<script lang="ts">
  import { page } from "$app/stores";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import { capitalize } from "$lib/utils/misc";

  export let data;

  const { service } = data;

  let currentLocation = "service-orientation-step1";
  if ($page.url.pathname.endsWith("/orienter/demande")) {
    currentLocation = "service-orientation-step2";
  } else if ($page.url.pathname.endsWith("/orienter/merci")) {
    currentLocation = "service-orientation-confirmation";
  }
</script>

<EnsureLoggedIn>
  <CenteredGrid bgColor="bg-france-blue">
    <div class="mb-s48 print:mb-s0">
      <Breadcrumb
        {service}
        structure={service.structureInfo}
        {currentLocation}
      />
    </div>
    <h1 class="text-white print:text-france-blue">
      Orienter un ou une bénéficiaire vers le service&nbsp;:
    </h1>
    <h2 class="text-white print:text-france-blue">
      {service.name}
    </h2>
    <h3 class=" text-white print:text-france-blue">
      <div><strong>{capitalize(service.structureInfo.name)}</strong></div>
    </h3>
  </CenteredGrid>

  <CenteredGrid bgColor="bg-white" roundedColor="bg-france-blue">
    <slot />
  </CenteredGrid>

  <slot name="navbar" />
</EnsureLoggedIn>
