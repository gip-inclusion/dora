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
    <div class="flex-[2] rounded-md border border-gray-02 md:relative">
      <div
        class="flex flex-wrap items-center justify-between gap-s12 border-b border-gray-02 px-s16 py-s20 md:px-s35"
      >
        <h1 class="m-s0 text-f23 leading-20 text-france-blue">
          Mes informations
        </h1>

        <LinkButton
          label="Modifier vos informations"
          to={`/auth/ic-update?next=${encodeURIComponent(
            `${getApiURL()}/mon-compte`
          )}`}
          icon={externalLinkIcon}
          iconOnRight
        />
      </div>

      <div class="grid gap-s35 p-s16 md:grid-cols-2 md:p-s35">
        <div>
          <h2 class="mb-s8 text-f20 leading-20 text-gray-dark">Prénom</h2>
          <div class="text-gray-text">{$userInfo.firstName}</div>
        </div>
        <div>
          <h2 class="mb-s8 text-f20 leading-20 text-gray-dark">Nom</h2>
          <div class="text-gray-text">{$userInfo.lastName}</div>
        </div>
        <div>
          <h2 class="mb-s8 text-f20 leading-20 text-gray-dark">Courriel</h2>
          <div class="text-gray-text">{$userInfo.email}</div>
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
      <ImproveDoraNotif />

      {#if $userInfo.isStaff}
        <div class="mb-s24 rounded-md  border border-gray-03 p-s24">
          <h4>Raccourcis</h4>
          <p class="text-f14">Pour l’équipe DORA.</p>
          <div class="flex flex-col gap-s8 lg:flex-row">
            <LinkButton
              label="Créer une structure"
              to="/structures/creer"
              secondary
              small
            />

            <LinkButton label="Administration" to="/admin" secondary small />
          </div>
        </div>
      {:else if $userInfo.isManager}
        <div class="mb-s24 rounded-md  border border-gray-03 p-s24">
          <h4>Raccourcis</h4>
          <div class="flex flex-col gap-s8 lg:flex-row">
            <LinkButton
              label="Tableau de bord département"
              to="/admin/structures"
              secondary
              small
            />
          </div>
        </div>
      {/if}
    </div>
  </div>
</EnsureLoggedIn>
