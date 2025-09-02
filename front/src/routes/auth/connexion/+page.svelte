<script lang="ts">
  import InformationLineSystem from "svelte-remix/InformationLineSystem.svelte";

  import { page } from "$app/state";

  import logoProConnect from "$lib/assets/proconnect/logo_proconnect.svg";
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import PcButton from "$lib/components/specialized/pc-button.svelte";

  import { getNextPage } from "../utils";
  import SendMagicLink from "./send-magic-link.svelte";

  const nextPage = getNextPage(page.url);

  let displayModal = $state(false);

  function handleOpenModal(event: MouseEvent) {
    event.preventDefault();
    displayModal = true;
  }
</script>

<CenteredGrid>
  <div class="mb-s48">
    <Breadcrumb currentLocation="login" />
  </div>

  <h1 class="mb-s24 text-france-blue">Accéder à DORA</h1>

  <div class="gap-s6 flex flex-col md:flex-row">
    <div class="flex-1">
      <FieldSet headerBg="bg-magenta-brand" noHeaderBorder noTopPadding>
        <div>
          <h2 class="mb-s32 text-france-blue">Se connecter ou s’inscrire</h2>
          <hr class="mb-s32" />
          <div class="mb-s24 bg-info-light p-s16 rounded-2xl">
            <h3 class="text-f17 text-info flex leading-24">
              <div class="mr-s8 h-s24 w-s24 inline-block fill-current">
                <InformationLineSystem />
              </div>
              <div>DORA utilise ProConnect</div>
            </h3>
            <p class="legend mb-s16 text-gray-text">
              <strong>Si vous avez déjà un compte Inclusion Connect,</strong> vous
              pouvez utiliser la même adresse e-mail pour accéder plus facilement
              à DORA.
            </p>
          </div>
          <PcButton {nextPage}>
            {#snippet pcHelpLink()}
              <a
                class="text-magenta-cta underline"
                target="_blank"
                title="Obtention d'un lien de connexion - ouverture dans une fenêtre modale"
                rel="noopener noreferrer"
                href="#"
                onclick={handleOpenModal}
              >
                Des difficultés à vous connecter&#8239;?
              </a>
            {/snippet}
          </PcButton>
        </div>
      </FieldSet>
    </div>

    <div class="flex-1">
      <div class="px-s64 py-s32">
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
          <p class="text-f14">🎉 Gagnez du temps sur vos démarches en ligne.</p>
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
      </div>
    </div>
  </div>

  <SendMagicLink bind:displayModal />
</CenteredGrid>
