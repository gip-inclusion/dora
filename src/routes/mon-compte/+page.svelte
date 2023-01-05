<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { userInfo } from "$lib/utils/auth";
  import ImproveDoraNotif from "./notif-improve.svelte";
</script>

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
      <ImproveDoraNotif />

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
