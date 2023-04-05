<script lang="ts">
  import { pageLineIcon } from "$lib/icons";
  import illuServices from "$lib/assets/illustrations/services.svg";
  import EmptyNotice from "../empty-notice.svelte";
</script>

<EmptyNotice
  textTopIcon={pageLineIcon}
  illustration={illuServices}
  title="Vous n’avez pas encore renseigné vos services sur DORA"
  links={[
    {
      url: "https://aide.dora.inclusion.beta.gouv.fr/fr/article/referencer-son-offre-de-service-xpivaw/",
      label: "Découvrez comment référencer son premier service",
    },
    {
      url: "https://aide.dora.inclusion.beta.gouv.fr/fr/category/conseils-1vz0ity/",
      label:
        "Découvrez quelques conseils sur la présentation de votre offre de service",
    },
    {
      url: "https://app.livestorm.co/dora-1",
      label: "Participez à un webinaire",
    },
    {
      url: "https://www.youtube.com/channel/UCadIsy9gfHgLmLkutRGC5ew/playlists",
      label: "Consultez les tutoriels",
    },
  ]}
>
  <div class="text-center leading-24">
    Pour rendre visibles vos services sur DORA — mais aussi sur les autres
    plateformes partenaires — vous devez saisir les informations de présentation
    et d’orientation avant de les publier. Vous pouvez à tout moment les mettre
    à jour, les remettre en brouillon ou les archiver si elles ne sont plus
    d’actualité.
  </div>
</EmptyNotice>
