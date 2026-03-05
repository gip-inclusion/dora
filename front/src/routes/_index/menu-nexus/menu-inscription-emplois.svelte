<script lang="ts">
  import { EMPLOIS_SIGNUP_PAGE_URL } from "$lib/env";

  import LinkButton from "$lib/components/display/link-button.svelte";

  import MenuInscriptionBase from "./menu-inscription-base.svelte";
</script>

<MenuInscriptionBase
  text="Pour accéder à votre portail, vous devez avoir un compte sur les Emplois de l’inclusion"
>
  <LinkButton
    label="S’inscrire aux Emplois de l’inclusion"
    to={EMPLOIS_SIGNUP_PAGE_URL}
    wFull
    extraClass="mb-s16"
  />
</MenuInscriptionBase>
