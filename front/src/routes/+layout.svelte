<script lang="ts">
  import type { Snippet } from "svelte";
  import { browser } from "$app/environment";
  import { beforeNavigate } from "$app/navigation";
  import { SvelteToast, toast } from "@zerodevx/svelte-toast";
  import { page } from "$app/stores";
  import { ENVIRONMENT } from "$lib/env";
  import "../app.css";
  import Footer from "./_index/footer.svelte";
  import Header from "./_index/header.svelte";
  import SkipLink from "./_index/skip-link.svelte";
  import UserOnboardingModal from "$lib/components/user/user-onboarding-modal.svelte";
  import { userInfo } from "$lib/utils/auth";
  import { trackPageView } from "$lib/utils/stats";
  import { enforceCrispConsent } from "$lib/utils/consent.svelte";
  import CookieBanner from "$lib/components/specialized/cookie-banner/cookie-banner.svelte";
  import { handleEmploisOrientation } from "$lib/utils/nexus";

  interface Props {
    children?: Snippet;
  }

  let { children }: Props = $props();

  $effect(() => {
    trackPageView($page.url.pathname, $page.data.title);
  });

  $effect(() => {
    $page.url;
    enforceCrispConsent();
  });

  $effect(() => {
    if (browser && $page.url.searchParams.get("link_expired") === "true") {
      toast.push("Lien expiré");
    }
  });

  $effect(() => {
    if (browser && $page.url.searchParams.has("op")) {
      handleEmploisOrientation($page.url);
    }
  });

  beforeNavigate(({ from, to }) => {
    if (!from || !to) return;

    const hasOrientation = from.url.searchParams.has("orientation");
    if (!hasOrientation) return;

    const isGoingToOrienter = to.url.pathname.match(/^\/services\/[^/]+\/orienter/);
    if (!isGoingToOrienter) {
      // Remove orientation param from history so back button doesn't retain it
      const cleanUrl = new URL(from.url);
      cleanUrl.searchParams.delete("orientation");
      history.replaceState({}, "", cleanUrl);
    }
  });
</script>

<svelte:head>
  {#key $page.data}
    {#if ENVIRONMENT !== "production" || $page.data.noIndex}
      <meta name="robots" content="noindex" />
    {/if}
    {#if $page.data.title}
      <title>{$page.data.title}</title>
    {:else}
      <title>DORA : recensement et mise à jour de l’offre d’insertion</title>
    {/if}
    {#if $page.data.description}
      <meta name="description" content={$page.data.description} />
    {:else if !$page.data.noIndex}
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
<SvelteToast />
