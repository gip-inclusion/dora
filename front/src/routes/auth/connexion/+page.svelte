<script lang="ts">
  import { preventDefault } from 'svelte/legacy';

  import { page } from "$app/stores";
  import logoC1 from "$lib/assets/inclusion-connect/logo-c1.svg";
  import logoDora from "$lib/assets/inclusion-connect/logo-dora-ic.svg";
  import logoInclusionConnect from "$lib/assets/illustrations/inclusion-connect.png";
  import logoProConnect from "$lib/assets/proconnect/logo_proconnect.svg";
  import logoCommunauteInclusion from "$lib/assets/inclusion-connect/logo-communaute-inclusion.svg";
  import logoRDVS from "$lib/assets/inclusion-connect/logo-rdv-solidarites.svg";
  import logoCNFS from "$lib/assets/inclusion-connect/logo-cnfs.svg";
  import logoIF from "$lib/assets/inclusion-connect/logo-if.svg";
  import logoMSS from "$lib/assets/inclusion-connect/logo-mss.svg";
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import { informationLineIcon } from "$lib/icons";
  import { getNextPage } from "../utils";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import IcButton from "$lib/components/specialized/ic-button.svelte";
  import PcButton from "$lib/components/specialized/pc-button.svelte";
  import { OIDC_AUTH_BACKEND } from "$lib/env";
  import SendMagicLink from "./send-magic-link.svelte";

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

  let displayModal = $state(false);
</script>

<CenteredGrid>
  <div class="mb-s48">
    <Breadcrumb currentLocation="login" dark />
  </div>

  <h1 class="mb-s24 text-france-blue">Accéder à DORA</h1>

  <div class="gap-s6 flex flex-col md:flex-row">
    <div class="flex-1">
      <FieldSet headerBg="bg-magenta-brand" noHeaderBorder noTopPadding>
        <div>
          <h2 class="mb-s32 text-france-blue">Se connecter ou s’inscrire</h2>
          <hr class="mb-s32" />

          <div class="mb-s24 bg-info-light p-s16 rounded-2xl">
            {#if OIDC_AUTH_BACKEND === "proconnect"}
              <h3 class="text-f17 text-info flex leading-24">
                <div class="mr-s8 h-s24 w-s24 inline-block fill-current">
                  {@html informationLineIcon}
                </div>
                <div>DORA utilise ProConnect</div>
              </h3>
              <p class="legend mb-s16 text-gray-text">
                <strong>Si vous avez déjà un compte Inclusion Connect,</strong> vous
                pouvez utiliser la même adresse e-mail pour accéder plus facilement
                à DORA.
              </p>
            {:else}
              <h3 class="text-f17 text-info flex leading-24">
                <div class="mr-s8 h-s24 w-s24 inline-block fill-current">
                  {@html informationLineIcon}
                </div>
                <div>DORA passe à Inclusion Connect&#8239;!</div>
              </h3>
              <p class="legend mb-s16 text-gray-text">
                <strong>Si vous aviez un ancien compte DORA,</strong> vous pouvez
                simplement vous inscrire à Inclusion Connect avec la même adresse
                e-mail pour retrouver vos données.
              </p>
              <p class="legend mb-s16 text-gray-text">
                <strong>Si vous avez déjà un compte Inclusion Connect,</strong> vous
                pouvez l’utiliser pour accéder plus facilement à DORA.
              </p>
            {/if}
          </div>

          {#if OIDC_AUTH_BACKEND === "proconnect"}
            <PcButton {nextPage}>
              <!-- @migration-task: migrate this slot by hand, `pc-help-link` is an invalid identifier -->
  <a
                slot="pc-help-link"
                class="text-magenta-cta underline"
                target="_blank"
                title="Obtention d'un lien de connexion - ouverture dans une fenêtre modale"
                rel="noopener noreferrer"
                href="#"
                onclick={preventDefault(() => {
                  displayModal = true;
                })}
              >
                Des difficultés à vous connecter&#8239;?
              </a>
            </PcButton>
          {:else}
            <IcButton {nextPage} {loginHint}></IcButton>
          {/if}
        </div>
      </FieldSet>
    </div>

    <div class="flex-1">
      <div class="px-s64 py-s32">
        {#if OIDC_AUTH_BACKEND === "proconnect"}
          <h3 class="text-france-blue text-center">
            <img src={logoProConnect} alt="ProConnect" class="mb-s8 mx-auto" />
            Pourquoi ProConnect&#8239;?
          </h3>
          <div class="mt-s24 text-center">
            <p class="text-f14 font-bold">
              🧑🏻‍💻 Un compte unique pour tous vos services numériques&#8239;!
            </p>
            <p class="text-f14">
              🔐 Accédez aux différents services partenaires avec le même
              identifiant et le même mot de passe.
            </p>
            <p class="text-f14">
              🎉 Gagnez du temps sur vos démarches en ligne.
            </p>
          </div>

          <hr class="my-s32" />

          <div class="text-f14 text-center">
            Pour en savoir plus sur <strong>ProConnect</strong>,
            <a
              class="text-magenta-cta underline"
              target="_blank"
              title="FAQ ProConnect - ouverture dans une nouvelle fenêtre"
              rel="noopener"
              href="https://agentconnect.crisp.help/fr/"
            >
              consultez la documentation.
            </a>
          </div>
        {:else}
          <h2 class="text-center">
            <img
              src={logoInclusionConnect}
              alt="Inclusion Connect"
              class="mb-s32 mx-auto"
            />
          </h2>
          <div class="mt-s24 text-center">
            <p class="text-f14 font-bold">
              🧑🏻‍💻 Un compte unique pour tous vos services numériques&#8239;!
            </p>
            <p class="text-f14">
              🔐 Accédez aux différents services partenaires avec le même
              identifiant et le même mot de passe.
            </p>
            <p class="text-f14">
              🎉 Gagnez du temps sur vos démarches en ligne.
            </p>
          </div>

          <hr class="my-s32" />
          <div
            class="around mb-s32 gap-x-s12 gap-y-s24 flex flex-wrap content-center items-center justify-center sm:flex-row"
          >
            <img
              class="inline-block grow-0"
              width="100"
              src={logoRDVS}
              alt="RDV Solidarités"
            />
            <img
              class="inline-block grow-0"
              width="100"
              src={logoC1}
              alt="Les emplois de l’inclusion"
            />
            <img
              class="inline-block flex-none"
              width="100"
              src={logoCommunauteInclusion}
              alt="La communauté de l’inclusion"
            />
            <img
              class="inline-block flex-none"
              width="100"
              src={logoDora}
              alt="DORA"
            />
            <img
              class="inline-block flex-none"
              width="100"
              src={logoIF}
              alt="immmersion facilitée"
            />
            <img
              class="inline-block flex-none"
              width="80"
              src={logoCNFS}
              alt="Conseiller numérique"
            />
            <img
              class="inline-block flex-none"
              width="100"
              src={logoMSS}
              alt="mon suivi social"
            />
          </div>

          <div class="text-f14 text-center">
            Pour en savoir plus sur <strong>Inclusion Connect</strong>,
            <a
              class="text-magenta-cta underline"
              target="_blank"
              title="Ouverture dans une nouvelle fenêtre"
              rel="noopener"
              href="https://aide.dora.inclusion.beta.gouv.fr/fr/article/inclusion-connect-quesaco-y13f84/"
            >
              consultez notre documentation.
            </a>
          </div>
        {/if}
      </div>
    </div>
  </div>

  <SendMagicLink bind:displayModal />
</CenteredGrid>
