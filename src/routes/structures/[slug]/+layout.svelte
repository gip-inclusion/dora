<script lang="ts">
  import cornerLeftVioletImg from "$lib/assets/corner-left-violet.png";
  import cornerRightVioletImg from "$lib/assets/corner-right-violet.png";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { TallyFormId } from "$lib/utils/nps";
  import Header from "./header.svelte";
  import { structure } from "./store";

  $: publishedServices = $structure.services.filter(
    (s) => s.status === "PUBLISHED"
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
  <TallyNpsPopup formId={TallyFormId.NPS_OFFEROR_FORM_ID} timeout={30000} />
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
