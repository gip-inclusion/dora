<script lang="ts">
  import type { Snippet } from "svelte";
  import { browser } from "$app/environment";
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
  import { TOAST_DURATION_MS } from "$lib/consts";
  import type { PageData } from "./$types";
  import {setCurrentStructure} from "$lib/utils/preferences";

  interface Props {
    children?: Snippet;
    data: PageData;
  }

  let { children, data }: Props = $props();

  $effect(() => {
    trackPageView($page.url.pathname, $page.data.title);
  });

  $effect(() => {
    $page.url;
    enforceCrispConsent();
  });

  $effect(() => {
    if (browser && $page.url.searchParams.get("link_invalid") === "true") {
      toast.push("Lien expiré ou invalide");
    }
  });

  $effect(() => {
    const userStructureSlug = $page.url.searchParams.get("user_structure_slug");
    if (userStructureSlug && $userInfo) {
      const userStructure = [
        ...$userInfo.pendingStructures,
        ...$userInfo.structures,
      ].find((struct) => struct.slug === userStructureSlug);

      if (userStructure && setCurrentStructure(userStructureSlug)) {
        toast.push(
          `Votre structure active a été automatiquement modifiée : vous utilisez désormais ${userStructure.name}.<br/><br/>Attention : si d'autres onglets DORA sont ouverts dans votre navigateur, votre activité dans ces onglets sera également associée à la structure ${userStructure.name}.`,
          { target: "structure-switch" }
        );
      }
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
  {#if $userInfo && !$userInfo.mainActivity && !data.hasOrientationJwt}
    <UserOnboardingModal />
  {/if}

  {@render children?.()}
</main>

<Footer />
<CookieBanner />
<SvelteToast options={{ duration: TOAST_DURATION_MS }} />
<div class="structure-switch-toast">
  <SvelteToast target="structure-switch" options={{ duration: TOAST_DURATION_MS }} />
</div>

<style>
  .structure-switch-toast :global(._toastContainer) {
    top: 6.6rem;
    left: 50%;
    right: auto;
    transform: translateX(-50%);
  }
  .structure-switch-toast :global(._toastItem) {
    width: 50vw
  }
</style>
