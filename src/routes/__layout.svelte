<script context="module">
  import { getUserInfo } from "$lib/auth";

  import * as Sentry from "@sentry/browser";

  import { SENTRY_DSN, ENVIRONMENT } from "$lib/env.js";

  if (ENVIRONMENT !== "local") {
    Sentry.init({
      dsn: SENTRY_DSN,
      environment: ENVIRONMENT,
      tracesSampleRate: 0,
    });
  }

  export async function load({ _page, _fetch, _session, _context }) {
    await getUserInfo();
    return {};
  }
</script>

<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { HOTJAR_ID, HOTJAR_SV } from "$lib/env";

  import favicoIco from "$lib/assets/favicon.ico";
  import favicoSvg from "$lib/assets/favicon.svg";
  import favicoPng from "$lib/assets/favicon.png";

  import "../app.postcss";

  import Footer from "./_layout/_footer.svelte";
  import Header from "./_layout/_header.svelte";

  onMount(() => {
    tarteaucitron.user.hotjarId = HOTJAR_ID;
    tarteaucitron.user.HotjarSv = HOTJAR_SV;
  });
</script>

<svelte:head>
  <link rel="icon" href={favicoIco} sizes="any" />
  <link rel="icon" href={favicoSvg} type="image/svg+xml" />
  <link rel="apple-touch-icon" href={favicoPng} />

  <script
    defer
    data-domain={$page.host}
    src="https://plausible.io/js/plausible.outbound-links.js"></script>
  <script>
    window.plausible =
      window.plausible ||
      function () {
        (window.plausible.q = window.plausible.q || []).push(arguments);
      };
  </script>

  {#if ENVIRONMENT !== "production"}
    <meta name="robots" content="noindex" />
  {/if}
</svelte:head>
<Header />

<main>
  <slot />
</main>

<Footer />
