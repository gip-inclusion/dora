<script>
  import { goto } from "$app/navigation";

  import { getApiURL } from "$lib/utils";
  import { token } from "$lib/auth";
  import Button from "$lib/components/button.svelte";
  import { arrowRightSIcon } from "$lib/icons.js";

  import { get } from "svelte/store";
  import { structureCache } from "./_creation-store.js";

  async function handleSubmit() {
    const url = `${getApiURL()}/structures/`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",

        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify(get(structureCache)),
    });

    if (res.ok) {
      const structure = await res.json();
      goto(`${structure.id}`);
    }

    return {
      status: res.status,
      error: new Error(`Could not load ${url}`),
    };
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <Button
    name="validate"
    type="submit"
    label="Validez les informations"
    icon={arrowRightSIcon}
    iconOnRight />
</form>
