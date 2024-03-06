<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import Header from "./header.svelte";

  import { TallyFormId } from "$lib/consts";
  import { structure } from "./store";

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
  <TallyPopup
    formId={TallyFormId.NPS_FORM_ID}
    timeoutSeconds={30}
    keySuffix="offreur"
    hiddenFields={{ user: "offreur" }}
  />
{/if}
