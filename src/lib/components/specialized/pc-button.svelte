<script lang="ts">
  import { getApiURL } from "$lib/utils/api";

  export let nextPage: string;

  const loginUrl =
    getApiURL() + "/oidc/login/?next=" + encodeURIComponent(nextPage);
</script>

<div class="text-center">
  <a class="mb-s24 inline-block" href={loginUrl}>
    <div
      class="proconnect-button mx-auto mt-s24 flex items-center justify-center rounded-full bg-france-blue p-s6 pr-s24 text-f16 text-white transition-colors hover:bg-[#2323FF]"
    ></div>
  </a>

  <div class="text-center">
    <a
      class="text-magenta-cta underline"
      target="_blank"
      title="Ouverture dans une nouvelle fenêtre"
      rel="noopener"
      href="https://aide.dora.inclusion.beta.gouv.fr"
    >
      Besoin d’aide&nbsp;? Contactez-nous (mais pas tout de suite)
    </a>
  </div>
</div>
