<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { externalLinkIcon } from "$lib/icons";
  import { getApiURL } from "$lib/utils/api";
  import { userInfo } from "$lib/utils/auth";
  import ImproveDoraNotif from "./notif-improve.svelte";
</script>

<EnsureLoggedIn>
  <div class="mb-s32">
    <Breadcrumb currentLocation="account" dark />
  </div>

  <div class="flex flex-col gap-s24 md:flex-row">
    <h1 class="sr-only">Mon compte</h1>
    <div class="flex-[2] rounded-md border border-gray-02 md:relative">
      <div
        class="flex flex-wrap items-center justify-between gap-s12 border-b border-gray-02 px-s16 py-s20 md:px-s35"
      >
        <h2 class="m-s0 text-f23 leading-20 text-france-blue">
          Mes informations
        </h2>

        <LinkButton
          label="Modifier vos informations"
          to={`/auth/ic-update?next=${encodeURIComponent(
            `${getApiURL()}/mon-compte`
          )}`}
          icon={externalLinkIcon}
          iconOnRight
        />
      </div>

      <div class="flex flex-col  gap-s35 p-s16 md:mb-s56 md:p-s35">
        <div class="flex w-full flex-col flex-wrap gap-s35 md:flex-row">
          <div class="flex-1">
            <h3 class="mb-s8 text-f18 leading-20">Prénom</h3>
            <div class="text-gray-text">{$userInfo.firstName}</div>
          </div>
          <div class="flex-1">
            <h3 class="mb-s8 text-f18 leading-20">Nom</h3>
            <div class="text-gray-text">{$userInfo.lastName}</div>
          </div>
        </div>
        <div>
          <h3 class="mb-s8 text-f18 leading-20">Courriel</h3>
          <div class="break-all text-gray-text">{$userInfo.email}</div>
        </div>
      </div>

      <div class="bottom-s0 w-full pt-s12 md:absolute">
        <hr class="mx-s12 md:mx-s35" />
        <p class="m-s0 py-s12 px-s16 text-f14 text-gray-text md:px-s35">
          Vous utilisez <a
            class="underline"
            href="https://aide.dora.inclusion.beta.gouv.fr/fr/article/inclusion-connect-quesaco-y13f84/"
            >Inclusion Connect</a
          > pour vous connecter à DORA.
        </p>
      </div>
    </div>

    <div class="flex flex-1 flex-col gap-s24">
      {#if $userInfo.isStaff}
        <div class="mb-s24 rounded-md  border border-gray-03 p-s24">
          <h2 class="mb-s20 text-f18 leading-20 text-gray-dark">Raccourcis</h2>

          <ul class="flex flex-col gap-s10">
            <li>
              <a
                class="text-f14 font-bold text-magenta-cta hover:underline"
                href="/structures/creer"
              >
                Créer une structure
              </a>
            </li>
            <li>
              <a
                class="text-f14 font-bold text-magenta-cta hover:underline"
                href="/admin"
              >
                Administration
              </a>
            </li>
          </ul>
        </div>
      {:else if $userInfo.isManager}
        <div class="mb-s24 rounded-md  border border-gray-03 p-s24">
          <h2 class="mb-s20 text-f18 leading-20 text-gray-dark">Raccourcis</h2>
          <div class="flex flex-col gap-s8 lg:flex-row">
            <a
              class="text-f14 font-bold text-magenta-cta hover:underline"
              href="/admin/structures"
            >
              Tableau de bord département
            </a>
          </div>
        </div>
      {/if}

      <ImproveDoraNotif />
    </div>
  </div>
</EnsureLoggedIn>
