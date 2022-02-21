<script>
  import { loginIcon, dashboardIcon, userFillIcon } from "$lib/icons.js";

  import LinkButton from "$lib/components/link-button.svelte";
  import TopLinks from "./_top-links.svelte";
</script>

<LinkButton
  label="Mon espace"
  to={`/tableau-de-bord`}
  icon={dashboardIcon}
  iconOnRight
  noBackground
/>
<LinkButton
  label="Mon profil"
  to={`/tableau-de-bord/profil`}
  icon={userFillIcon}
  iconOnRight
  noBackground
/>
<LinkButton
  label="Deconnexion"
  to={`/auth/deconnexion`}
  icon={loginIcon}
  iconOnRight
  noBackground
/>
<div class="block md:hidden">
  <div class="border-t border-gray-01" />
  <TopLinks />
</div>
