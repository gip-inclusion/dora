<script lang="ts">
  import { page } from "$app/stores";
  import { closeIcon, informationLine } from "$lib/icons";
  import LinkButton from "$lib/components/link-button.svelte";

  export let isOpen;
</script>

<div
  class="relative flex w-full flex-col items-start sm:flex-row sm:items-center sm:justify-between"
>
  <button
    aria-label="Supprimer le message"
    on:click={() => (isOpen = false)}
    class="absolute right-s10 block h-s24 w-s24"
  >
    <span class="h-s24 w-s24 fill-current text-magenta-cta">
      {@html closeIcon}
    </span>
  </button>

  <div class="mr-s10 mb-s16 flex items-center sm:mb-s0">
    <span
      class="mr-s10 hidden h-s24 w-s24 fill-current text-service-blue-info md:block"
    >
      {@html informationLine}
    </span>
    <div class="flex flex-col">
      <span class="pr-s40 font-bold text-service-blue-info"
        >Pour mobiliser ce service, vous devez vous connecter !</span
      >
      <p class="mb-s0 hidden text-f14 text-gray-text lg:inline">
        En vous connectant, vous aurez accès aux informations de contact afin de
        mobiliser ce service pour votre bénéficiaire.
      </p>
    </div>
  </div>

  <div class="w-full sm:w-auto sm:pr-s80">
    <LinkButton
      wFull
      label="Se connecter"
      nofollow
      to={`/auth/connexion?next=${encodeURIComponent($page.url.pathname)}`}
    />
  </div>
</div>
