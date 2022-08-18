<script context="module">
  import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";
  import { disconnect } from "$lib/auth";

  export async function load({ url }) {
    const query = url.searchParams;

    const token = query.get("token");
    const targetUrl = `${getApiURL()}/auth/registration/validate-email/`;

    const result = await fetch(targetUrl, {
      method: "POST",
      headers: {
        Accept: defaultAcceptHeader,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ key: token }),
    });

    const validated = result.ok;

    if (validated) {
      // log out of the current session in case we were already connected with
      // a different account
      disconnect();
    }

    return {
      props: { validated },
    };
  }
</script>

<script>
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Info from "$lib/components/info.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import AuthLayout from "./_auth_layout.svelte";

  export let validated;

  function handleClickConnexionButton() {
    plausible("inscription", { props: { step: "Validation après création" } });
  }
</script>

<svelte:head>
  <title>Valider votre compte | DORA</title>
</svelte:head>

<CenteredGrid>
  <div class="text-center">
    <h1 class="text-france-blue">Créer son compte DORA</h1>
  </div>
</CenteredGrid>

<AuthLayout>
  <Fieldset title="Accédez à votre compte">
    {#if validated}
      <Info label="Inscription complète !" positiveMood>
        <p class="mb-s16">
          Utilisez l’adresse courriel et le mot de passe saisis lors de
          l’inscription pour vous connecter.
        </p>
      </Info>
      <LinkButton
        to="/auth/connexion"
        label="Aller à la page de connexion"
        on:click={handleClickConnexionButton}
      />
    {:else}
      <Info label="Le lien a expiré ou n’est pas valide" negativeMood />
      <LinkButton
        to="/auth/renvoyer-email-validation"
        label="Demander un nouveau lien"
      />
    {/if}
  </Fieldset>
</AuthLayout>
