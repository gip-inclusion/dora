<script context="module">
  export const ssr = false;

  import { get } from "svelte/store";
  import { token } from "$lib/auth";
  import { getNextPage } from "./utils.js";

  export async function load({ url }) {
    const nextPage = getNextPage(url);
    // Si on a déjà un token, on redirige directement sur la destination
    if (get(token)) {
      return {
        status: 302,
        redirect: nextPage,
      };
    }
    return {};
  }
</script>

<script>
  import { page } from "$app/stores";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import Button from "$lib/components/button.svelte";

  import AuthLayout from "./_auth_layout.svelte";
  import { informationLineIcon } from "$lib/icons.js";

  import PoleEmploiWarning from "$lib/components/structures/pole-emploi-warning.svelte";
  import logoIC from "$lib/assets/inclusion-connect/logo-inclusion-connect.svg";
  import logoC1 from "$lib/assets/inclusion-connect/logo-c1.svg";
  import logoDora from "$lib/assets/inclusion-connect/logo_dora.svg";
  import logoPEFill from "$lib/assets/logo-pole-emploi-fill.svg";

  function getLoginHint() {
    const loginHint = $page.url.searchParams.get("login_hint");

    if (loginHint) {
      $page.url.searchParams.delete("login_hint");
      return `&login_hint=${encodeURIComponent(loginHint)}`;
    }
    return "";
  }

  const loginHint = getLoginHint();
  const nextPage = getNextPage($page.url);

  let showPEMessage = false;

  function togglePEMessage() {
    showPEMessage = !showPEMessage;
  }

  $: togglePEMessageLabel = showPEMessage ? "Réduire" : "Lire la suite";
</script>

<svelte:head>
  <title>Connexion / Inscription | DORA</title>
</svelte:head>

<AuthLayout>
  <FieldSet headerBg="bg-magenta-brand" noHeaderBorder noTopPadding>
    <div class="flex-1">
      <h2 class="mb-s32 text-france-blue">Accédez à votre compte</h2>

      <div class="rounded-ml bg-info-light p-s16">
        <h4 class="flex text-info">
          <div class="mr-s8 inline-block h-s24 w-s24 fill-current">
            {@html informationLineIcon}
          </div>
          <div>DORA passe à Inclusion Connect&nbsp!</div>
        </h4>
        <div class="legend mb-s16 text-gray-text">
          Si vous avez un Compte DORA, il vous suffit de créer un compte
          Inclusion Connect avec la même adresse e-mail afin de retrouver les
          mêmes droits et données.
        </div>
      </div>

      <div class="mt-s16  rounded-ml bg-info-light p-s16">
        <div class="legend mb-s16 flex gap-s16 text-f14 text-gray-text">
          <img src={logoPEFill} alt="" width="46" height="46" />
          Agents Pôle emploi, vous n’avez pas besoin de créer de compte.
        </div>
        {#if showPEMessage}
          <PoleEmploiWarning />
        {/if}

        <Button
          label={togglePEMessageLabel}
          on:click={togglePEMessage}
          noBackground
          small
          noPadding
          hoverUnderline
        />
      </div>

      <p class="mt-s24 mb-s24" />
      <div class="mb-s40">
        <a
          href="/auth/ic-connect?next={encodeURIComponent(nextPage)}{loginHint}"
        >
          <div
            class="mx-auto flex items-center justify-center rounded bg-[#000638] px-s12 py-s12 text-f16 font-bold text-white "
          >
            <img src={logoIC} alt="" width="32" height="35" />
            <div class="ml-s10">S’identifier avec Inclusion Connect</div>
          </div>
        </a>

        <div class="my-s24 text-center">
          <a
            class="text-magenta-cta underline"
            target="_blank"
            title="Ouverture dans une nouvelle fenêtre"
            rel="noopener nofollow noreferrer"
            href="https://aide.dora.fabrique.social.gouv.fr/fr/category/inscription-et-gestion-du-compte-ha8m5b/"
          >
            Besoin d’aide&nbsp;? Contactez-nous
          </a>
        </div>

        <hr class="my-s24 " />

        <div class="flex h-s35 items-center justify-center gap-s48 ">
          <img
            width="126"
            height="36"
            src={logoC1}
            alt="Les emplois de l'inclusion, la communauté de l'inclusion, DORA"
          />
          <img
            width="126"
            height="36"
            src={logoDora}
            alt="Les emplois de l'inclusion, la communauté de l'inclusion, DORA"
          />
        </div>
        <div class="mt-s24 text-center">
          Avec <strong>Inclusion Connect</strong> vous pouvez accéder aux différents
          services partenaires avec le même identifiant et mot de passe.
        </div>
        <div class="text-center">
          <a
            class="text-magenta-cta underline"
            target="_blank"
            rel="noopener nofollow noreferrer"
            href="https://aide.dora.fabrique.social.gouv.fr/fr/article/inclusion-connect-quesaco-y13f84/"
          >
            En savoir plus
          </a>
        </div>
      </div>
    </div>
  </FieldSet>
</AuthLayout>
