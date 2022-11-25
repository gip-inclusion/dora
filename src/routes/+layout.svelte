<script lang="ts">
  import { ENVIRONMENT } from "$lib/env";
  import "../app.postcss";
  import Footer from "./layout/footer.svelte";
  import Header from "./layout/header.svelte";
  import SkipLink from "./layout/skip-link.svelte";
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
