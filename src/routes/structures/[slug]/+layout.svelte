<script lang="ts">
  import cornerLeftVioletImg from "$lib/assets/style/corner-left-violet.png";
  import cornerRightVioletImg from "$lib/assets/style/corner-right-violet.png";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import TallyNpsPopup from "$lib/components/specialized/tally-nps-popup.svelte";
  import { TallyFormId } from "$lib/utils/nps";
  import Header from "./header.svelte";
  import { structure } from "./store";

  $: publishedServices = $structure.services.filter(
    (service) => service.status === "PUBLISHED"
  );
</script>

<CenteredGrid bgColor="bg-magenta-brand" noPadding>
  <Header structure={$structure} />
</CenteredGrid>

<div class="relative hidden w-full md:block">
  <img
    src={cornerLeftVioletImg}
    alt=""
    class="md absolute top-s0 left-s0 print:hidden"
  />
  <img
    src={cornerRightVioletImg}
    alt=""
    class="top-0 absolute right-s0 print:hidden"
  />
</div>

<CenteredGrid>
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

<style lang="postcss">
  img {
    zoom: 0.6;
  }

  @screen xl {
    img {
      zoom: 1;
    }
  }
</style>
