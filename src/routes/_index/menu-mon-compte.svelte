<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import {
    accountCircleLineIcon,
    logoutBoxLineIcon,
    starSmileLineIcon,
  } from "$lib/icons";
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
