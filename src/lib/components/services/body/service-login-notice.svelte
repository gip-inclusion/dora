<script lang="ts">
  import { page } from "$app/stores";
  import LinkButton from "$lib/components/link-button.svelte";

  export let isOpen;
</script>

<div class="flex w-full flex-col rounded-lg bg-info-light p-s16">
  <div class="mb-s8 text-f17 font-bold text-service-blue-info">
    Pour mobiliser ce service, vous devez vous connecter&nbsp;!
  </div>
  <div class="mb-s24 text-f14 text-gray-text">
    En vous connectant, vous aurez accès aux informations de contact afin de
    mobiliser ce service pour votre bénéficiaire.
  </div>

  <div>
    <LinkButton
      small
      label="Se connecter"
      nofollow
      to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
    />
  </div>
</div>
