<script context="module">
  import { getStructure } from "$lib/structures";
  import { trackStructure } from "$lib/utils/plausible";
  import { structure } from "./_store";
  import { userPreferences } from "$lib/preferences";
  import { userInfo } from "$lib/auth";

  export async function load({ params }) {
    const s = await getStructure(params.slug);
    let preferences;
    let info;

    userPreferences.subscribe((p) => {
      preferences = p;
    });

    userInfo.subscribe((u) => {
      info = u;
    });

    if (preferences) {
      const userStructuresSlugs = [
        ...info.pendingStructures,
        ...info.structures,
      ].map((us) => us.slug);

      if (userStructuresSlugs.includes(s.slug)) {
        const slugIndex = preferences.visitedStructures.indexOf(s.slug);

        if (slugIndex > 0) {
          preferences.visitedStructures.splice(slugIndex, 1);
        }

        preferences.visitedStructures.unshift(s.slug);

        localStorage.setItem(
          "visitedStructures",
          JSON.stringify(preferences.visitedStructures)
        );

        userPreferences.set(preferences);
      }
    }

    if (!s) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    structure.set(s);
    trackStructure(s);

    return {};
  }
</script>

<script lang="ts">
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";

  import cornerLeftVioletImg from "$lib/assets/corner-left-violet.png";
  import cornerRightVioletImg from "$lib/assets/corner-right-violet.png";
  import { NPS_OFFEROR_FORM_ID } from "$lib/const";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
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

{#if $structure.isMember}
  <TallyNpsPopup formId={NPS_OFFEROR_FORM_ID} timeout={30000} />
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
