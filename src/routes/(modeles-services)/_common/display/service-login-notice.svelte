<script lang="ts">
  import { page } from "$app/stores";
  import LinkButton from "$lib/components/display/link-button.svelte";
</script>

<div class="mb-s24 text-f14 text-white">
  Pour accéder aux informations de contact de ce service, vous devez vous
  connecter.
</div>

<div>
  <LinkButton
    extraClass="bg-white !text-france-blue hover:!text-white tracking-tight"
    label="S’identifier avec Inclusion Connect"
    to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
    canWrap
  />
</div>
