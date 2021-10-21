<script context="module">
  // We don't need ssr here, and don't want to api call done twice
  // given that the token will be deleted after validation
  export const ssr = false;

  import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";
  import { disconnect } from "$lib/auth";

  export async function load({ page, _fetch, _session, _context }) {
    const token = page.query.get("token");
    const url = `${getApiURL()}/auth/registration/validate-email/`;
    const result = await fetch(url, {
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
  import connexionPic from "$lib/assets/illu_connexion-optimise.svg";

  export let validated;
</script>

<CenteredGrid topPadded>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Créer son compte DORA</h1>
  </div>
</CenteredGrid>

<CenteredGrid roundedbg>
  <div class="col-span-full flex  lg:col-end-7 lg:mb-4 mt-6">
    <img src={connexionPic} alt="" class="max-w-xl justify-self-center" />
  </div>
  <div class="col-span-full lg:col-start-8 lg:col-end-12 mb-4">
    <Fieldset title="Accédez à votre compte">
      {#if validated}
        <Info label="Inscription complète !" positiveMood>
          <p class="mb-2">
            Utilisez l’adresse e-mail et le mot de passe saisis lors de
            l’inscription pour vous connecter.
          </p>
        </Info>
        <LinkButton
          to="/auth/connexion"
          label="Aller à la page de connexion"
          preventDefaultOnMouseDown
        />
      {:else}
        <Info label="Le lien a expiré ou n’est pas valide" negativeMood />
        <LinkButton
          to="/auth/renvoyer-email-validation"
          label="Demander un nouveau lien"
          preventDefaultOnMouseDown
        />
      {/if}
    </Fieldset>
  </div>
</CenteredGrid>
