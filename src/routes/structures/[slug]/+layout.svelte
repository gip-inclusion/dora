<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import TallyNpsPopup from "$lib/components/specialized/tally-nps-popup.svelte";
  import { TallyFormId } from "$lib/utils/nps";
  import type { PageData } from "./$types";
  import Header from "./header.svelte";
  import { structure } from "./store";

  export let data: PageData;

  $: publishedServices = $structure.services.filter(
    (service) => service.status === "PUBLISHED"
  );
</script>

<CenteredGrid bgColor="bg-magenta-brand print:bg-white" noPadding>
  <Header structure={$structure} />
</CenteredGrid>

<CenteredGrid roundedColor="bg-magenta-brand">
  <slot />
</CenteredGrid>

{#if $structure.isMember && publishedServices.length}
  <TallyNpsPopup
    formId={TallyFormId.NPS_FORM_ID}
    timeoutSeconds={30}
    keySuffix="offreur"
    hiddenFields={{ user: "offreur" }}
  />
{/if}
