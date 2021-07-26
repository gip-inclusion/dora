<script>
  import { goto } from "$app/navigation";
  import { browser } from "$app/env";

  import { getApiURL } from "$lib/utils";
  import { token } from "$lib/auth";

  import { service } from "./_creation-store.js";

  import { storageKey } from "./_constants.js";

  import arrowRightIcon from "remixicon/icons/System/arrow-right-line.svg?raw";

  function persistStore() {
    if (browser) {
      localStorage.setItem(storageKey, JSON.stringify($service));
    }
  }

  function clearStore() {
    localStorage.removeItem(storageKey);
  }

  async function handleValidate() {
    persistStore();
    const url = `${getApiURL()}/services/`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",

        Authorization: `Token ${$token}`,
      },
      body: JSON.stringify($service),
    });

    if (res.ok) {
      const service = await res.json();
      clearStore();
      goto(`../${service.id}`);
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  }
</script>

<button
  on:click|preventDefault={handleValidate}
  class="flex flex-row w-32 p-2 px-4 text-center text-white border-2 rounded bg-action disabled:bg-back2 ">
  <div>Valider</div>
  <div class="relative w-5 ml-3 fill-current top-1">
    {@html arrowRightIcon}
  </div>
</button>
