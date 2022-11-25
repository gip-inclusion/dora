<script lang="ts">
  import { ENVIRONMENT } from "$lib/env";
  import "../app.postcss";

  import Footer from "./_layout/_footer.svelte";
  import Header from "./_layout/_header.svelte";
  import SkipLink from "./_layout/_skip-link.svelte";
</script>

<svelte:head>
  {#if ENVIRONMENT !== "production"}
    <meta name="robots" content="noindex" />
  {/if}
</svelte:head>

<SkipLink />
<Header />

<main id="main-content">
  <slot />
</main>

<Footer />
