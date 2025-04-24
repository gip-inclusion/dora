<script lang="ts">
  import { API_URL } from "$lib/env";
  import logoPC from "$lib/assets/proconnect/bouton_proconnect.svg";

  export let nextPage: string;

  const loginUrl = `${API_URL}/oidc/login/?next=${encodeURIComponent(nextPage)}`;
</script>

<div class="text-center">
  <a class="mb-s24 inline-block" href={loginUrl}>
    <img src={logoPC} alt="" class="max-w-none" />
  </a>

  <div class="text-center">
    <slot name="pc-help-link">
      <a
        class="text-magenta-cta underline"
        target="_blank"
        title="Aide DORA - ouverture dans une nouvelle fenêtre"
        rel="noopener noreferrer"
        href="https://aide.dora.inclusion.beta.gouv.fr/fr/category/inscription-et-gestion-du-compte-ha8m5b/"
      >
        Besoin d’aide&#8239;? Contactez-nous
      </a>
    </slot>
    &nbsp;
    <a
      class="text-magenta-cta underline"
      target="_blank"
      title="Qu’est-ce que ProConnect&#8239;? nouvelle fenêtre"
      rel="noopener noreferrer"
      href="https://www.proconnect.gouv.fr/"
    >
      Qu'est que ProConnect&#8239;?
    </a>
  </div>
</div>
