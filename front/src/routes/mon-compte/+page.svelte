<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { userInfo } from "$lib/utils/auth";
  import ImproveDoraNotif from "./notif-improve.svelte";
</script>

<EnsureLoggedIn>
  <div class="mb-s32">
    <Breadcrumb currentLocation="account" />
  </div>

  <div class="gap-s24 flex flex-col md:flex-row">
    <h1 class="sr-only">Mon compte</h1>
    <div class="border-gray-02 flex-2 rounded-lg border md:relative">
      <div
        class="gap-s12 border-gray-02 px-s16 py-s20 md:px-s36 flex flex-wrap items-center justify-between border-b"
      >
        <h2 class="m-s0 text-f23 text-france-blue leading-20">
          Mes informations
        </h2>
      </div>

      <div class="gap-s36 p-s16 md:mb-s56 md:p-s36 flex flex-col">
        <div class="gap-s36 flex w-full flex-col flex-wrap md:flex-row">
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
          <div class="text-gray-text break-all">{$userInfo.email}</div>
        </div>
      </div>

      <div class="bottom-s0 pt-s12 w-full md:absolute">
        <hr class="mx-s12 md:mx-s36" />

        <p class="m-s0 px-s16 py-s12 text-f14 text-gray-text md:px-s36">
          Vous utilisez <a
            class="underline"
            href="https://agentconnect.crisp.help/fr/"
            rel="noopener noreferrer"
            target="_blank">ProConnect</a
          > pour vous connecter à DORA.
        </p>
      </div>
    </div>

    <div class="gap-s24 flex flex-1 flex-col">
      {#if $userInfo.isStaff || $userInfo.isManager}
        <div class="mb-s24 border-gray-03 p-s24 rounded-lg border">
          <h2 class="mb-s20 text-f18 text-gray-dark leading-20">Raccourcis</h2>
          <ul class="gap-s10 flex flex-col">
            {#if $userInfo.isStaff}
              <li>
                <a
                  class="text-f14 text-magenta-cta font-bold hover:underline"
                  href="/admin"
                >
                  Administration
                </a>
              </li>
              <li>
                <a
                  class="text-f14 text-magenta-cta font-bold hover:underline"
                  href="/admin/structures/creer"
                >
                  Créer une structure
                </a>
              </li>
            {:else if $userInfo.isManager}
              <li>
                <a
                  class="text-f14 text-magenta-cta font-bold hover:underline"
                  href="/admin/structures"
                >
                  Tableau de bord département
                </a>
              </li>
            {/if}
          </ul>
        </div>
      {/if}

      <ImproveDoraNotif />
    </div>
  </div>
</EnsureLoggedIn>
