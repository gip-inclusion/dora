<script lang="ts">
  import BookReadLineDocument from "svelte-remix/BookReadLineDocument.svelte";

  import illuModeles from "$lib/assets/illustrations/modeles.svg";
  import EmptyNotice from "../empty-notice.svelte";
  import { URL_HELP_SITE } from "$lib/consts";
</script>

<EmptyNotice
  textTopIcon={BookReadLineDocument}
  illustration={illuModeles}
  title="Vous n’avez pas encore créé votre premier modèle"
  links={[
    {
      url: `${URL_HELP_SITE}article/creer-des-modeles-et-dupliquer-ses-services-1ts5cd7/`,
      label: "Découvrez comment créer un modèle et l’utiliser",
    },
  ]}
>
  <div class="text-center leading-24">
    Les modèles vous permettent de créer facilement plusieurs services
    similaires. Un exemple&nbsp;: vous avez des services identiques sur
    différents lieux d’accueil — la création d’un modèle va vous faciliter la
    saisie de vos services.
  </div>

  <div class="mt-s20 text-center leading-24">
    Vous aurez de plus la possibilité de synchroniser le modèle avec les
    services, afin de faciliter la mise à jour des informations en commun.
  </div>
</EmptyNotice>
