<script lang="ts">
  import { page } from "$app/stores";
  import logoC1 from "$lib/assets/inclusion-connect/logo-c1.svg";
  import logoDora from "$lib/assets/inclusion-connect/logo-dora-ic.svg";
  import logoInclusionConnect from "$lib/assets/illustrations/inclusion-connect.png";
  import logoCommunauteInclusion from "$lib/assets/inclusion-connect/logo-communaute-inclusion.svg";
  import logoIC from "$lib/assets/inclusion-connect/logo-inclusion-connect.svg";
  import logoRDVS from "$lib/assets/inclusion-connect/logo-rdv-solidarites.svg";
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import { informationLineIcon } from "$lib/icons";
  import { getNextPage } from "../utils";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";

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

<CenteredGrid>
  <div class="mb-s48">
    <Breadcrumb currentLocation="login" dark />
  </div>

  <h1 class="mb-s24 text-france-blue">Accéder à DORA</h1>

  <div class="flex flex-col gap-s6 md:flex-row">
    <div class="flex-1">
      <FieldSet headerBg="bg-magenta-brand" noHeaderBorder noTopPadding>
        <div>
          <h2 class="mb-s32 text-france-blue">Se connecter ou s‘inscrire</h2>
          <hr class="mb-s32" />

          <div class="mb-s24 rounded-ml bg-info-light p-s16">
            <h3 class="flex text-f17 leading-24 text-info">
              <div class="mr-s8 inline-block h-s24 w-s24 fill-current">
                {@html informationLineIcon}
              </div>
              <div>DORA passe à Inclusion Connect&nbsp!</div>
            </h3>
            <p class="legend mb-s16 text-gray-text">
              <strong>Si vous aviez un ancien compte DORA,</strong> vous pouvez simplement
              vous inscrire à Inclusion Connect avec la même adresse e-mail pour
              retrouver vos données.
            </p>
            <p class="legend mb-s16 text-gray-text">
              <strong>Si vous avez déjà un compte Inclusion Connect,</strong> vous
              pouvez l‘utiliser pour accéder plus facilement à DORA.
            </p>
          </div>

          <div class="text-center">
            <a
              class="mb-s24 inline-block"
              href="/auth/ic-connect?next={encodeURIComponent(
                nextPage
              )}{loginHint}"
            >
              <div
                class="mx-auto mt-s24 flex items-center justify-center rounded-full bg-france-blue p-s6 pr-s24 text-f16 text-white transition-colors hover:bg-[#2323FF]"
              >
                <span class="h-[62px] w-[62px] rounded-full bg-white p-s6">
                  <img src={logoIC} alt="" class="max-w-none" />
                </span>
                <div class="ml-s16 text-left">
                  S‘identifier avec <strong class="whitespace-nowrap">
                    Inclusion Connect
                  </strong>
                </div>
              </div>
            </a>

            <div class="text-center">
              <a
                class="text-magenta-cta underline"
                target="_blank"
                title="Ouverture dans une nouvelle fenêtre"
                rel="noopener"
                href="https://aide.dora.inclusion.beta.gouv.fr/fr/category/inscription-et-gestion-du-compte-ha8m5b/"
              >
                Besoin d’aide&nbsp;? Contactez-nous
              </a>
            </div>
          </div>
        </div>
      </FieldSet>
    </div>

    <div class="flex-1">
      <div class="px-s64 py-s32">
        <h2 class="text-center">
          <img
            src={logoInclusionConnect}
            alt="Inclusion Connect"
            class="mx-auto mb-s32"
          />
        </h2>
        <div class="mt-s24 text-center">
          <p class="text-f14 font-bold">
            🧑🏻‍💻 Un compte unique pour tous vos services numériques !
          </p>
          <p class="text-f14">
            🔐 Accédez aux différents services partenaires avec le même
            identifiant et le même mot de passe.
          </p>
          <p class="text-f14">🎉 Gagnez du temps sur vos démarches en ligne.</p>
        </div>

        <hr class="my-s32" />
        <div
          class="mb-s32 flex flex-wrap content-center items-center justify-around gap-s8 sm:flex-row"
        >
          <img
            class="inline-block"
            width="100"
            height="36"
            src={logoRDVS}
            alt="RDV Solidarités"
          />
          <img
            class="inline-block"
            width="100"
            height="36"
            src={logoC1}
            alt="Les emplois de l‘inclusion"
          />
          <img
            class="inline-block"
            width="100"
            height="36"
            src={logoCommunauteInclusion}
            alt="La communauté de l‘inclusion"
          />
          <img
            class="inline-block"
            width="80"
            height="36"
            src={logoDora}
            alt="DORA"
          />
        </div>

        <div class="text-center text-f14">
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
      </div>
    </div>
  </div>
</CenteredGrid>
