<script>
  import {
    accountCircleLineIcon,
    starSmileLineIcon,
    logoutBoxLineIcon,
  } from "$lib/icons.js";

  import LinkButton from "$lib/components/link-button.svelte";
</script>

<LinkButton
  label="Mon compte"
  to={`/mon-compte`}
  icon={accountCircleLineIcon}
  iconOnRight
  noBackground
  small
/>

<LinkButton
  label="Mes favoris"
  to={`/favoris`}
  icon={starSmileLineIcon}
  iconOnRight
  noBackground
  small
/>

<LinkButton
  label="Déconnexion"
  to={`/auth/deconnexion`}
  icon={logoutBoxLineIcon}
  iconOnRight
  noBackground
  small
/>
