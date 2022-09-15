<script>
  import { userInfo, userInfoIsComplete } from "$lib/auth";

  import LinkButton from "$lib/components/link-button.svelte";
  import EnsureLoggedIn from "$lib/components/ensure-logged-in.svelte";
  import ImproveDoraNotif from "./_notif-improve.svelte";
</script>

<svelte:head>
  <title>Mon compte | DORA</title>
</svelte:head>

<EnsureLoggedIn>
  <div class="mb-s24 md:flex md:items-center md:justify-between">
    <h2 class="text-france-blue">Mon compte</h2>
    <div class="flex gap-s12">
      <LinkButton label="Modifier" to="/mon-compte/editer" small />
    </div>
  </div>

  <div class="md:flex md:gap-s24">
    <div class="mb-s24 flex-1 rounded-md bg-gray-00 p-s24">
      <h3>{$userInfo.fullName}</h3>
      <p>{$userInfo.phoneNumber}</p>
      <p>{$userInfo.email}</p>
    </div>

    <div class="flex flex-1 flex-col gap-s24">
      {#if userInfoIsComplete()}
        <ImproveDoraNotif />
      {/if}

      {#if $userInfo.isStaff || $userInfo.isBizdev}
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
      {/if}
    </div>
  </div>
</EnsureLoggedIn>
