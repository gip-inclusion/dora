<script>
  import { onMount } from "svelte";
  import { token } from "$lib/auth";
  import { getApiURL } from "$lib/utils";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";

  import { serviceOptions } from "./_creation-store.js";
  import NavLink from "./_navlink.svelte";

  onMount(async () => {
    const url = `${getApiURL()}/services/`;
    const res = await fetch(url, {
      method: "OPTIONS",
      headers: {
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });

    if (res.ok) {
      $serviceOptions = (await res.json()).actions.POST;
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  });
</script>

<style>
  h1 + p {
    margin-top: var(--s16);
    color: var(--col-text);
    font-size: var(--f16);
    line-height: var(--s24);
  }

  nav {
    display: flex;
    justify-content: center;
    margin-top: var(--s24);
  }
</style>

<EnsureLoggedIn>
  <CenteredGrid>
    <div class="col-start-1 col-span-full text-center mb-6">
      <div class="mx-auto">
        <h1 class="text-france-blue text-13xl">Ajouter un service</h1>
        <p class="text-gray-text text-base">
          Rendez visible votre offre de services sur la plateforme DORA.<br />
          Les champs marqués d’un astérisque<span
            style="color: var(--col-error);">*</span> sont obligatoires.
        </p>

        <nav>
          <NavLink target="etape1" name="Présentation du service" />
          <NavLink target="etape2" name="Conditions d’accès" />
          <NavLink target="etape3" name="Modalités d’accès" />
          <NavLink target="etape4" name="Informations pratiques" />
        </nav>
      </div>
    </div>
  </CenteredGrid>

  <CenteredGrid gridRow="2" roundedbg>
    <div class="col-span-8 col-start-1 mb-8">
      <slot name="content" />
    </div>
  </CenteredGrid>

  <CenteredGrid gridRow="3" sticky>
    <slot name="navbar" />
  </CenteredGrid>
</EnsureLoggedIn>
