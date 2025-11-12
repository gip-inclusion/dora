<script lang="ts">
  import Button from "$lib/components/display/button.svelte";

  interface Props {
    handleAcceptAll: () => void;
    handleRejectAll: () => void;
    handlePersonalize: () => void;
  }

  let { handleAcceptAll, handleRejectAll, handlePersonalize }: Props = $props();
</script>

<div
  class="mx-s4 md:mx-s0 bottom-s40 md:left-s40 py-s32 px-s4 md:px-s32 fixed z-[9999] bg-white shadow-md"
>
  <div class="md:w-[588px]">
    <h2 class="text-gray-dark mb-s32 text-[1.5rem]">
      À propos des cookies sur dora.inclusion.gouv.fr
    </h2>
    <p class="mb-s32 leading-relaxed text-gray-600">
      Bienvenue ! Nous utilisons des cookies pour améliorer votre expérience et
      les services disponibles sur ce site. Pour en savoir plus, visitez la page
      <a
        href="politique-de-confidentialite"
        class="text-f18 text-magenta-cta underline"
      >
        Données personnelles et cookies.
      </a>
      Vous pouvez, à tout moment, avoir le contrôle sur les cookies que vous souhaitez
      activer.
    </p>

    <div class="gap-s4 md:gap-s16 flex w-full justify-end">
      <Button label="Personnaliser" secondary onclick={handlePersonalize}
      ></Button>
      <Button label="Tout refuser" onclick={handleRejectAll}></Button>
      <Button label="Tout accepter" onclick={handleAcceptAll}></Button>
    </div>
  </div>
</div>
