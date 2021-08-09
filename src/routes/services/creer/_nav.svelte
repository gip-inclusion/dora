<script>
  import { goto } from "$app/navigation";
  import { browser } from "$app/env";

  import { getApiURL } from "$lib/utils";
  import { token } from "$lib/auth";
  import NavButtons from "$lib/components/nav-buttons.svelte";

  import { get } from "svelte/store";
  import { storageKey } from "./_constants.js";
  import { serviceCache } from "./_creation-store.js";

  export let withBack = false;
  export let withForward = false;
  export let withValidate = false;
  export let backlink, forwardlink;

  export function persistStore() {
    if (browser) {
      localStorage.setItem(storageKey, JSON.stringify(get(serviceCache)));
    }
  }

  function clearStore() {
    localStorage.removeItem(storageKey);
  }

  export async function handleSubmit() {
    console.log($serviceCache);
    const body = get(serviceCache);
    const url = `${getApiURL()}/services/`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",

        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify(body),
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

  function persistAndGo(evt) {
    persistStore();
    if (evt.submitter.name === "backward") {
      goto(backlink);
    } else if (evt.submitter.name === "forward") {
      goto(forwardlink);
    } else if (evt.submitter.name === "validate") {
      handleSubmit();
    } else {
      console.log("Invalid submitter button name", evt.submitter.name);
    }
  }
</script>

<NavButtons
  {withBack}
  {withForward}
  {withValidate}
  {backlink}
  {forwardlink}
  on:submit={persistAndGo} />
