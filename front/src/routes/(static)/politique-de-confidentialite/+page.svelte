<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import StaticMarkdown from "$lib/components/display/static-markdown.svelte";
  import type { PageData } from "./$types";
  import { showCookieBanner } from "$lib/utils/consent.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
</script>

<CenteredGrid>
  <div class="mb-s48">
    <Breadcrumb currentLocation="privacy" />
  </div>

  <StaticMarkdown content={data.content} />

  <div class="mt-s48 max-w-3xl">
    <p>
      DORA utilise également la solution de mesure d’audience
      <a href="https://matomo.org/" class="underline">Matomo</a> en l’ayant
      configuré en mode « exempté », conformément aux
      <a
        href="https://www.cnil.fr/fr/solutions-pour-la-mesure-daudience"
        class="underline">recommandations de la CNIL</a
      >. Elle ne nécessite donc pas le consentement des personnes concernées.
      Vous pouvez malgré tout vous opposer au suivi de votre navigation via
      <button class="text-magenta-cta underline" onclick={showCookieBanner}
        >le gestionnaire de cookies</button
      >.
    </p>
  </div>
</CenteredGrid>
