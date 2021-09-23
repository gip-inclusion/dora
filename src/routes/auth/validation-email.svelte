<script context="module">
  // We don't need ssr here, and don't want to api call done twice
  // given that the token will be deleted after validation
  export const ssr = false;
  import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";

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

    return {
      props: { validated },
    };
  }
</script>

<script>
  import Fieldset from "$lib/components/forms/fieldset.svelte";
  import Info from "./_info.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import connexionPic from "$lib/assets/illu_connexion-optimise.svg";

  export let validated;
</script>

<CenteredGrid>
  <div class="col-start-1 mb-6 text-center col-span-full">
    <h1 class="text-france-blue text-13xl">Créer son compte DORA</h1>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="2" roundedbg>
  <div class="col-start-1 col-end-7 mb-4 mt-6">
    <img src={connexionPic} alt="" />
  </div>
  <div class="col-start-7 col-end-13 mb-4">
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
          preventDefaultOnMouseDown />
      {:else}
        <Info label="Le lien a expiré ou n’est pas valide" negativeMood />
        <LinkButton
          to="/auth/renvoyer-email-validation"
          label="Demander un nouveau lien"
          preventDefaultOnMouseDown />
      {/if}
    </Fieldset>
  </div>
</CenteredGrid>
