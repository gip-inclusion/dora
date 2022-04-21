<script context="module">
  import { getStructure } from "$lib/structures";

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
          "structuresViewed",
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

    return {};
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";
</script>

<CenteredGrid --col-bg="var(--col-magenta-brand)" topPadded>
  <div class="col-span-full">
    <Header structure={$structure} />
  </div>
</CenteredGrid>

<CenteredGrid
  roundedTop
  --col-under-bg="var(--col-magenta-brand)"
  --col-content-bg="var(--col-bg)"
  topPadded
>
  <slot />
</CenteredGrid>
