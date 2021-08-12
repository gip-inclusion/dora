<script>
  import { goto } from "$app/navigation";

  import { getApiURL } from "$lib/utils";
  import { token } from "$lib/auth";
  import Button from "$lib/components/button.svelte";
  import { arrowRightSIcon } from "$lib/icons.js";

  import { get } from "svelte/store";

  export let structure;
  async function handleSubmit() {
    const url = `${getApiURL()}/structures/`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",

        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify(structure),
    });

    if (res.ok) {
      const createdStructure = await res.json();
      goto(`${createdStructure.slug}`);
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
