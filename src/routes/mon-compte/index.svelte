<script>
  import { userInfo, userInfoIsComplete } from "$lib/auth";

  import LinkButton from "$lib/components/link-button.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import UpdateProfileNotif from "./_notif-incomplete.svelte";
  import ImproveDoraNotif from "./_notif-improve.svelte";
</script>

<svelte:head>
  <title>Mon compte | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <div class="col-span-full md:flex md:items-center md:justify-between">
    <h2 class="mb-s24 text-france-blue">Mon compte</h2>
    <div class="flex gap-s16">
      <LinkButton label="Modifier…" to="/mon-compte/editer" small />

      <LinkButton
        label="Changer de mot de passe…"
        to="/mon-compte/mot-de-passe"
        secondary
        small
      />
    </div>
  </div>

  <div class="col-span-full md:flex md:gap-s24">
    <div class="mb-s24 flex-1 rounded-md bg-gray-00 p-s24">
      <h3>{$userInfo.fullName}</h3>
      <p>{$userInfo.phoneNumber}</p>
      <p>{$userInfo.email}</p>
    </div>

    <div class="flex-1">
      <div
        class="mb-s24 rounded-md border border-gray-03 p-s24 lg:flex lg:flex-row lg:justify-between lg:gap-s16"
      >
        {#if !userInfoIsComplete()}
          <UpdateProfileNotif />
        {:else}
          <ImproveDoraNotif />
        {/if}
      </div>

      {#if $userInfo.isStaff || $userInfo.isBizdev}
        <div class="mb-s24 rounded-md  border border-gray-03 p-s24">
          <h4>Raccourcis</h4>
          <p class="text-f14">Pour l’équipe DORA.</p>
          <div class="flex flex-col gap-s8 lg:flex-row">
            <LinkButton
              label="Créer une structure…"
              to="/structures/creer"
              secondary
              small
            />

            <LinkButton label="Structures" to="/structures" secondary small />

            <LinkButton label="Services" to="/services" secondary small />

            <LinkButton
              label="Suggestions de service"
              to="/services-suggestions"
              secondary
              small
            />
          </div>
        </div>
      {/if}
    </div>
  </div>
</EnsureLoggedIn>
