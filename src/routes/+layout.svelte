<script lang="ts">
  import { ENVIRONMENT } from "$lib/env";
  import favicoIco from "$lib/assets/favicon.ico";
  import favicoSvg from "$lib/assets/favicon.svg";
  import favicoPng from "$lib/assets/favicon.png";

  import "../app.postcss";

  import Footer from "./_layout/_footer.svelte";
  import Header from "./_layout/_header.svelte";
  import SkipLink from "./_layout/_skip-link.svelte";
</script>

<svelte:head>
  <link rel="icon" href={favicoIco} sizes="any" />
  <link rel="icon" href={favicoSvg} type="image/svg+xml" />
  <link rel="apple-touch-icon" href={favicoPng} />
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
