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
  import { page } from "$app/stores";

  import "../app.postcss";
  import "../app.css";

  import Footer from "./_layout/_footer.svelte";
  import Header from "./_layout/_header.svelte";
</script>

<svelte:head>
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

<main class="global-content-wrapper grid row-start-2">
  <slot />
</main>

<Footer />
