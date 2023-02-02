<script lang="ts">
  import { page } from "$app/stores";
  import logoC1 from "$lib/assets/inclusion-connect/logo-c1.svg";
  import logoDora from "$lib/assets/inclusion-connect/logo-dora-ic.svg";
  import logoIC from "$lib/assets/inclusion-connect/logo-inclusion-connect.svg";
  import logoRDVS from "$lib/assets/inclusion-connect/logo-rdv-solidarites.svg";
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import { informationLineIcon } from "$lib/icons";
  import AuthLayout from "../auth-layout.svelte";
  import { getNextPage } from "../utils";

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
</script>

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

        <div
          class="flex flex-col items-center justify-between gap-s32 sm:flex-row sm:gap-s16"
        >
          <img width="126" height="36" src={logoRDVS} alt="RDV Solidarités" />
          <img
            width="126"
            height="36"
            src={logoC1}
            alt="Les emplois de l'inclusion"
          />
          <img width="126" height="36" src={logoDora} alt="DORA" />
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
