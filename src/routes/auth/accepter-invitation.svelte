<script context="module">
  import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";
  import { disconnect } from "$lib/auth";

  export async function load({ url }) {
    const query = url.searchParams;

    const inviteToken = query.get("token");
    const membershipId = query.get("membership");
    const targetUrl = `${getApiURL()}/structure-putative-members/${membershipId}/accept-invite/`;
    const method = "POST";
    const result = await fetch(targetUrl, {
      method,
      headers: {
        Accept: defaultAcceptHeader,
        Authorization: `Token ${inviteToken}`,
      },
    });
    if (result.ok) {
      // log out of the current session in case we were already connected with
      // a different account
      disconnect();

      const jsonResult = await result.json();
      return {
        props: {
          validated: true,
          mustSetPassword: jsonResult.mustSetPassword,
          structureName: jsonResult.structureName,
          resetToken: jsonResult.token,
        },
      };
    }
    return {
      props: { validated: false },
    };
  }
</script>

<script>
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Info from "$lib/components/info.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import AuthLayout from "./_auth_layout.svelte";

  export let validated, mustSetPassword, structureName, resetToken;
</script>

<svelte:head>
  <title>Rejoindre une structure | DORA</title>
</svelte:head>

<CenteredGrid topPadded>
  <div class="col-span-full col-start-1 mb-s48 text-center">
    <h1 class="text-france-blue">Rejoindre une structure</h1>
  </div>
</CenteredGrid>

<AuthLayout>
  <Fieldset title="Accédez à votre compte">
    {#if validated}
      <Info label="Vous avez rejoint la structure {structureName}" positiveMood>
        {#if !mustSetPassword}
          <p class="mb-s16">
            Utilisez l’adresse courriel et le mot de passe saisis lors de
            l’inscription pour vous connecter.
          </p>
        {/if}
      </Info>
      {#if mustSetPassword}
        <LinkButton
          label="Choisissez votre mot de passe"
          to="/auth/reinitialiser-mdp?token={resetToken}"
        />
      {:else}
        <LinkButton
          to="/auth/connexion"
          label="Aller à la page de connexion"
          preventDefaultOnMouseDown
        />
      {/if}
    {:else}
      <Info label="Le lien a expiré ou n’est pas valide" negativeMood>
        <p>
          Contactez l’administrateur de votre structure pour en obtenir un
          nouveau
        </p>
      </Info>
    {/if}
  </Fieldset>
</AuthLayout>
