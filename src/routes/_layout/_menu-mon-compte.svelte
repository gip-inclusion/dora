<script>
  import { loginIcon, userFillIcon } from "$lib/icons.js";

  import LinkButton from "$lib/components/link-button.svelte";
</script>

<LinkButton
  label="Mon compte"
  to={`/mon-compte`}
  icon={userFillIcon}
  iconOnRight
  noBackground
  small
/>

<LinkButton
  label="Déconnexion"
  to={`/auth/deconnexion`}
  icon={loginIcon}
  iconOnRight
  noBackground
  small
/>
