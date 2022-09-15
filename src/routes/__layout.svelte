<script context="module">
  import { get } from "svelte/store";
  import { browser } from "$app/env";
  import { CRISP_ID } from "$lib/env";
  import { userInfo, validateCredsAndFillUserInfo } from "$lib/auth";

  import * as Sentry from "@sentry/browser";

  import { ENVIRONMENT, SENTRY_DSN } from "$lib/env.js";

  if (ENVIRONMENT !== "local") {
    Sentry.init({
      dsn: SENTRY_DSN,
      environment: ENVIRONMENT,
      tracesSampleRate: 0,
    });
  }

  export async function load({ url }) {
    await validateCredsAndFillUserInfo();
    const currentUserInfo = get(userInfo);
    if (
      currentUserInfo &&
      !(
        currentUserInfo.structures.length ||
        currentUserInfo.pendingStructures.length
      ) &&
      !url.pathname.startsWith("/auth/rattachement") &&
      !url.pathname.startsWith("/auth/deconnexion")
    ) {
      return {
        status: 302,
        redirect: "/auth/rattachement",
      };
    }
    return {};
  }

  if (browser) {
    tarteaucitron.user.crispID = CRISP_ID;
  }
</script>

<script>
  import { page } from "$app/stores";

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

  <script async src="https://tally.so/widgets/embed.js"></script>
  <script
    defer
    data-domain={$page.url.hostname}
    src="https://plausible.io/js/plausible.js"></script>
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

<SkipLink />
<Header />

<main id="main-content">
  <slot />
</main>

<Footer />
