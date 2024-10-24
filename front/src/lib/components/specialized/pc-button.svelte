<script lang="ts">
  import { getApiURL } from "$lib/utils/api";
  import logoPC from "$lib/assets/proconnect/bouton_proconnect.svg";

  export let nextPage: string;

  const loginUrl =
    getApiURL() + "/oidc/login/?next=" + encodeURIComponent(nextPage);
</script>

<div class="text-center">
  <a class="mb-s24 inline-block" href={loginUrl}>
    <img src={logoPC} alt="" class="max-w-none" />
  </a>

  <div class="text-center">
    <a
      class="text-magenta-cta underline"
      target="_blank"
      title="Aide DORA - ouverture dans une nouvelle fenêtre"
      rel="noopener noreferrer"
      href="https://aide.dora.inclusion.beta.gouv.fr/fr/category/inscription-et-gestion-du-compte-ha8m5b/"
    >
      Besoin d’aide&nbsp;? Contactez-nous
    </a>
    &nbsp;
    <a
      class="text-magenta-cta underline"
      target="_blank"
      title="Qu’est-ce que ProConnect ? nouvelle fenêtre"
      rel="noopener noreferrer"
      href="https://www.proconnect.gouv.fr/"
    >
      Qu'est que ProConnect&nbsp;?
    </a>
  </div>
</div>
