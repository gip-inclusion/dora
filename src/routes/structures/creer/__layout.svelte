<script>
  import { onMount } from "svelte";

  import { page } from "$app/stores";
  import { goto } from "$app/navigation";

  import { token } from "$lib/auth";
  import { getApiURL } from "$lib/utils";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import { structureOptions } from "./_creation-store.js";

  onMount(async () => {
    if (!$token) {
      goto(`/login?next=${encodeURIComponent($page.path)}`);
      return;
    }
    const url = `${getApiURL()}/structures/`;
    const res = await fetch(url, {
      method: "OPTIONS",
      headers: {
        Accept: "application/json; version=1.0",
        Authorization: `Token ${$token}`,
      },
    });

    if (res.ok) {
      $structureOptions = (await res.json()).actions.POST;
      console.log($structureOptions);
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  });
</script>

<CenteredGrid class1="col-start-1 row-start-1 col-span-full">
  <div class="col-start-1 col-span-full text-center mb-6">
    <h1 class="text-france-blue text-13xl">Création d’une structure</h1>
    <p class="text-gray-text text-base">
      Rendez visible vos offres de services sur la plateforme DORA.
    </p>
  </div>
</CenteredGrid>

<CenteredGrid
  class1="col-start-1 row-start-2 rounded-t-xl col-span-full bg-gray-bg">
  <div class="col-span-8 col-start-1 mb-4">
    <slot />
  </div>
</CenteredGrid>
