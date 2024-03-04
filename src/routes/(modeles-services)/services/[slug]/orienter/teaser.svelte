<script lang="ts">
  import { checkboxCircleFillIcon } from "$lib/icons";
  import { page } from "$app/stores";
  import IcButton from "$lib/components/specialized/ic-button.svelte";

  const nextURL = new URL($page.url);
  nextURL.searchParams.set("newlogin", "1");
</script>

<h2>Accédez au formulaire d’orientation</h2>

<div class="mt-s40 flex flex-col-reverse gap-s24 lg:flex-row">
  <div
    class="flex basis-2/3 flex-col gap-s40 rounded-ml border border-gray-01 p-s32"
  >
    <h3 class="mb-s0 text-france-blue">
      Pourquoi utiliser le formulaire d’orientation DORA
    </h3>
    <ul class="line text-f18 leading-40">
      <li>
        <span class="checkbox">{@html checkboxCircleFillIcon}</span>Orientez
        vers la solution identifié en moins de 5 minutes
      </li>
      <li>
        <span class="checkbox">{@html checkboxCircleFillIcon}</span>Incluez le
        bénéficiaire dans la démarche
      </li>
      <li>
        <span class="checkbox">{@html checkboxCircleFillIcon}</span>Recevez des
        notifications sur l'avancement de votre demande
      </li>
      <li>
        <span class="checkbox">{@html checkboxCircleFillIcon}</span>Suivez
        toutes vos demandes grâce au tableau de bord
        <span
          class="ml-s4 inline-block h-s24 rounded bg-magenta-brand px-s8 py-s2 align-baseline text-f12 leading-20 text-white"
        >
          BIENTÔT
        </span>
      </li>
    </ul>

    <hr class="border-t-gray-01" />
    <div>
      <h4>Curieux d’en savoir plus ?</h4>
      <p>
        Découvrez le formulaire d’orientation grâce a notre vidéo de
        démonstration :
      </p>
      <div style="position: relative; padding-top: 50%;">
        <iframe
          title="DORA - Orienter un bénéficiaire"
          width="100%"
          height="100%"
          src="https://tube.numerique.gouv.fr/videos/embed/c620b3c6-d9c8-46aa-8ab6-42b14b3f45a0?subtitle=fr&amp;warningTitle=0&amp;peertubeLink=0&amp;p2p=0"
          frameborder="0"
          allowfullscreen
          sandbox="allow-same-origin allow-scripts allow-popups"
          style="position: absolute; inset: 0px;"
        ></iframe>
      </div>
    </div>
  </div>
  <div class="basis-1/3">
    <div class="flex flex-col rounded-ml border border-gray-01 p-s32">
      <h3 class="mb-s32 text-france-blue">Se connecter ou s’inscrire</h3>
      <hr class="mb-s32 border-t-gray-01" />
      <p class="text-f16">
        Il est nécessaire d'être connecté pour utiliser le formulaire
        d’orientation ou afficher les coordonnées de contact.
      </p>

      <IcButton
        nextPage={encodeURIComponent(nextURL.pathname + nextURL.search)}
      />
    </div>
  </div>
</div>

<style lang="postcss">
  .checkbox {
    @apply mr-s8 inline-block h-s24 w-s24 fill-current align-text-bottom text-success;
  }
</style>
