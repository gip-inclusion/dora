<script lang="ts">
  import { page } from "$app/stores";
  import { ENVIRONMENT } from "$lib/env";
  import "../app.postcss";
  import Footer from "./_index/footer.svelte";
  import Header from "./_index/header.svelte";
  import SkipLink from "./_index/skip-link.svelte";
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
  <slot />
</main>

<Footer />
