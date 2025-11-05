<script lang="ts">
  import type { Snippet } from "svelte";
  import { SvelteToast } from "@zerodevx/svelte-toast";
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
<SvelteToast />
