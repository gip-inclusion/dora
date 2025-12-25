<script lang="ts">
  import PagesLineDocument from "svelte-remix/PagesLineDocument.svelte";

  import illuServices from "$lib/assets/illustrations/services.svg";
  import EmptyNotice from "../empty-notice.svelte";
  import { URL_HELP_SITE } from "$lib/consts";
</script>

<EmptyNotice
  textTopIcon={PagesLineDocument}
  illustration={illuServices}
  title="Vous n’avez pas encore renseigné vos services sur DORA"
  links={[
    {
      url: `${URL_HELP_SITE}article/referencer-son-offre-de-service-xpivaw/`,
      label: "Découvrez comment référencer son premier service",
    },
    {
      url: `${URL_HELP_SITE}category/conseils-1vz0ity/`,
      label:
        "Découvrez quelques conseils sur la présentation de votre offre de service",
    },
    {
      url: `${URL_HELP_SITE}article/participer-a-un-webinaire-dora-h3n747/`,
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
