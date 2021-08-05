<script>
  import { onMount } from "svelte";

  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import { token } from "$lib/auth";
  import { getApiURL } from "$lib/utils";

  import { serviceOptions } from "./_creation-store.js";
  import NavLink from "./_navlink.svelte";

  onMount(async () => {
    if (!$token) {
      goto(`/login?next=${encodeURIComponent($page.path)}`);
      return;
    }
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

<div class="col-start-1 col-span-full">
  <h1>Votre solution d’accompagnement</h1>

  <nav class="flex flex-row">
    <NavLink target="etape1" name="1. Descriptif" />
    <NavLink target="etape2" name="2. Condition d’accès du bénéficiaire" />
    <NavLink target="etape3" name="3. Modalité d’accès à la solution" />
    <NavLink target="etape4" name="4. Informations pratiques" />
  </nav>

  <slot />
</div>
