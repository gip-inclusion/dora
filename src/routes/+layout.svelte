<script lang="ts">
  import { ENVIRONMENT } from "$lib/env";
  import "../app.postcss";
  import Footer from "./footer.svelte";
  import Header from "./header.svelte";
  import SkipLink from "./skip-link.svelte";
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
