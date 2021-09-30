<script context="module">
  import { getUserInfo } from "$lib/auth";
  import { ENVIRONMENT } from "$lib/env.js";

  // import * as Sentry from "@sentry/browser";
  // import { Integrations } from "@sentry/tracing";
  // import { SENTRY_DSN, ENVIRONMENT } from "$lib/env.js";

  // if (ENVIRONMENT !== "local") {
  //   Sentry.init({
  //     dsn: SENTRY_DSN,
  //     environment: ENVIRONMENT, // ,
  //     integrations: [new Integrations.BrowserTracing()],

  //     // Set tracesSampleRate to 1.0 to capture 100%
  //     // of transactions for performance monitoring.
  //     // We recommend adjusting this value in production
  //     tracesSampleRate: 1.0,
  //   });
  // }

  export async function load({ _page, _fetch, _session, _context }) {
    await getUserInfo();
    return {};
  }
</script>

<script>
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import NavItem from "$lib/components/nav-item.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import "../app.postcss";
  import "../app.css";
  import LogoRF from "$lib/assets/logo-rf.svg";
  import LogoDORA from "$lib/assets/dora-logo-rvb.svg";
  import LogoMinistere from "$lib/assets/logo-ministere-travail.svg";

  import MenuActions from "./_menu_actions.svelte";
</script>

<svelte:head>
  <script
    defer
    data-domain={$page.host}
    src="https://plausible.io/js/plausible.js"></script>

  {#if ENVIRONMENT !== "production"}
    <meta name="robots" content="noindex" />
  {/if}
</svelte:head>

<header class="grid row-start-1 shadow-md z-10 relative noprint">
  <CenteredGrid>
    <div class="flex flex-row items-center row-start-1 col-span-full py-3/2 ">
      <a class="flex flex-row gap-5 " href="/">
        <img
          class="inline"
          src={LogoMinistere}
          alt=""
          width="114"
          height="89" />
        <img class="inline" src={LogoDORA} alt="Dora" width="140" height="65" />
      </a>
      <div class="flex-grow" />
      <div class="flex flex-row">
        <MenuActions />
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid gridRow="2" bordertop>
    <div class="flex flex-row col-span-full">
      <NavItem
        label="Communauté de l’inclusion"
        href="https://communaute.inclusion.beta.gouv.fr/"
        external />
      <NavItem
        label="Contacter l’équipe"
        href="https://itou.typeform.com/doracontactsupp" />
    </div>
  </CenteredGrid>
</header>

<div class="global-content-wrapper grid row-start-2">
  <slot />
</div>

<footer class="grid row-start-3 border-t-2 border-france-blue pt-5/2 noprint">
  <CenteredGrid>
    <div class="col-span-5 mb-5">
      <img class="inline" src={LogoRF} alt="" width="124" height="110" />
    </div>
    <div class="col-span-6 col-start-7 text-sm leading-normal text-gray-text">
      Dora est un service public numérique qui permet aux structures de
      l’insertion de référencer simplement et mettre à jour en temps réel leur
      offre de services, et aux professionnels prescripteurs de rechercher et
      mobiliser rapidement le service le plus adapté au besoin de leur
      bénéficiaire.
      <div class="flex gap-3 mt-2 font-bold">
        <a target="_blank" rel="noopener" href="https://gouvernement.fr"
          >gouvernement.fr</a>
        <a target="_blank" rel="noopener" href="https://service-public.fr"
          >service-public.fr</a>
        <a target="_blank" rel="noopener" href="https://data.gouv.fr"
          >data.gouv.fr</a>
      </div>
    </div>
  </CenteredGrid>
  <CenteredGrid gridRow="2" bordertop>
    <div class="flex col-start-1 col-span-full">
      <NavItem href="" label="Plan du site" separator light />
      <NavItem href="" label="Accessibilité" separator light />
      <NavItem
        href=""
        label="Mentions légales"
        on:click={() => goto("/mentions-legales")}
        separator
        light />
      <NavItem href="" label="Données personnelles" separator light />
      <NavItem href="" label="Gestion des cookies" light />
    </div>
  </CenteredGrid>
</footer>
