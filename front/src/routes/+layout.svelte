<script lang="ts">
  import type { Snippet } from "svelte";
  import { browser } from "$app/env";
  import { SvelteToast } from "@zerodevx/svelte-toast";
  import { replaceState } from "$app/navigation";
  import { page } from "$app/state";
  import { ENVIRONMENT } from "#lib/env.ts";
  import "../app.css";
  import Footer from "./_index/footer.svelte";
  import Header from "./_index/header.svelte";
  import SkipLink from "./_index/skip-link.svelte";
  import UserOnboardingModal from "#lib/components/user/user-onboarding-modal.svelte";
  import { userInfo } from "#lib/utils/auth.ts";
  import { trackPageView } from "#lib/utils/stats.ts";
  import { enforceCrispConsent } from "#lib/utils/consent.svelte.ts";
  import CookieBanner from "#lib/components/specialized/cookie-banner/cookie-banner.svelte";
  import { TOAST_DURATION_MS } from "#lib/consts.ts";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();

  const LEGACY_ORIENTATION_JWT_PARAM = "op";

  $effect(() => {
    trackPageView(page.url.pathname, page.data.title);
  });

  $effect(() => {
    page.url;
    enforceCrispConsent();
  });

  // Les anciens liens des Emplois portaient un JWT (`op`) contenant les
  // données du bénéficiaire : on le retire de l'URL pour qu'il ne reste ni
  // dans l'historique ni dans les rapports d'erreur.
  $effect(() => {
    if (browser && page.url.searchParams.has(LEGACY_ORIENTATION_JWT_PARAM)) {
      const cleanUrl = new URL(page.url.href);
      cleanUrl.searchParams.delete(LEGACY_ORIENTATION_JWT_PARAM);
      cleanUrl.searchParams.delete("user_structure_slug");
      replaceState(cleanUrl, page.state);
    }
  });
</script>

<svelte:head>
  {#key page.data}
    {#if ENVIRONMENT !== "production" || page.data.noIndex}
      <meta name="robots" content="noindex" />
    {/if}
    {#if page.data.title}
      <title>{page.data.title}</title>
    {:else}
      <title>DORA : recensement et mise à jour de l’offre d’insertion</title>
    {/if}
    {#if page.data.description}
      <meta name="description" content={page.data.description} />
    {:else if !page.data.noIndex}
      <meta
        name="description"
        content="Le service public numérique de recensement et mise à jour de l’offre d’insertion."
      />
    {/if}
  {/key}
</svelte:head>

<SkipLink />
<Header />

<main id="main-content">
  {#if $userInfo && !$userInfo.mainActivity}
    <UserOnboardingModal />
  {/if}

  {@render children?.()}
</main>

<Footer />
<CookieBanner />
<SvelteToast options={{ duration: TOAST_DURATION_MS }} />
