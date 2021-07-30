<script>
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { getApiURL } from "$lib/utils";
  import { token, setToken } from "$lib/auth";
  import { onMount } from "svelte";

  import Button from "$lib/components/button.svelte";

  const next = $page.query.get("next") || "/";

  let email = "";
  let password = "";

  const handleSubmit = async () => {
    const url = `${getApiURL()}/api-token-auth/`;
    const result = await fetch(url, {
      method: "POST",
      body: JSON.stringify({
        username: email,
        password,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });

    if (result.ok) {
      const jsonResult = await result.json();
      setToken(jsonResult.token);
      await goto(next || "/");
    }
    return {
      status: result.status,
      error: new Error(`Could not load ${url}`),
    };
  };

  const validateMessageEmail = (event) => {
    let textbox = event.target;
    if (textbox.value === "") {
      textbox.setCustomValidity("Ce champ est requis");
    } else if (textbox.validity.typeMismatch) {
      textbox.setCustomValidity(
        "Merci de renseigner une adresse de couriel valide"
      );
    } else {
      textbox.setCustomValidity("");
    }
    return true;
  };

  onMount(() => {
    if ($token && $page.path === "/login") {
      goto(next);
    }
  });
</script>

<h1 class="mt-20 mb-4 text-4xl font-bold text-center">Se connecter</h1>
<form
  class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-gray-01"
  on:submit|preventDefault={handleSubmit}>
  <label class="flex flex-row items-center">
    <span class="inline-block w-40 font-bold">Couriel</span>
    <input
      class="flex-grow inline-block border-gray-02"
      type="email"
      required
      bind:value={email}
      on:invalid={validateMessageEmail} />
  </label>

  <label class="flex flex-row items-center">
    <span class="inline-block w-40 font-bold">Mot de passe</span>
    <input
      class="flex-grow inline-block border-gray-02"
      type="password"
      required
      bind:value={password}
      aria-live="polite" />
  </label>

  <Button type="submit" disabled={!email || !password} label="Connexion" />
</form>
