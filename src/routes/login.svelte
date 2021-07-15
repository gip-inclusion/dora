<script context="module">
  export const load = async ({ page }) => ({
    props: {
      next: page.query.get("next"),
    },
  });
</script>

<script>
  import { getApiURL } from "$lib/utils";
  import { goto } from "$app/navigation";
  import { setToken } from "$lib/auth";

  export let next;

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
</script>

<h1 class="mt-20 mb-4 text-4xl font-bold text-center">Se connecter</h1>
<form
  class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-back2"
  on:submit|preventDefault={handleSubmit}>
  <label class="flex flex-row items-center">
    <span class="inline-block w-40 font-bold">Couriel</span>
    <input
      class="flex-grow inline-block border-gray-300"
      type="email"
      required
      bind:value={email}
      on:invalid={validateMessageEmail} />
  </label>

  <label class="flex flex-row items-center">
    <span class="inline-block w-40 font-bold">Mot de passe</span>
    <input
      class="flex-grow inline-block border-gray-300"
      type="password"
      required
      bind:value={password}
      aria-live="polite" />
  </label>

  <button
    type="submit"
    disabled={!email || !password}
    class="self-end block w-32 p-2 px-4 text-white border-2 rounded bg-action disabled:bg-back2 ">
    Connexion
  </button>
</form>
