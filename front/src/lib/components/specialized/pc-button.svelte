<script lang="ts">
  import type { Snippet } from "svelte";

  import { getApiURL } from "$lib/utils/api";
  import logoPC from "$lib/assets/proconnect/bouton_proconnect.svg";
  import { PROCONNECT_MORE_INFO_URL, URL_HELP_SITE } from "$lib/consts";

  interface Props {
    nextPage: string;
    noHelpSection?: boolean;
    pcHelpLink?: Snippet;
  }

  let { nextPage, noHelpSection = false, pcHelpLink }: Props = $props();

  const loginUrl = `${getApiURL()}/oidc/login/?next=${encodeURIComponent(nextPage)}`;
</script>

<div class="text-center">
  <a class={[!noHelpSection && "mb-s24", "inline-block"]} href={loginUrl}>
    <img src={logoPC} alt="" class="max-w-none" />
  </a>

  {#if !noHelpSection}
    <div class="text-center">
      {#if pcHelpLink}
        {@render pcHelpLink()}
      {:else}
        <a
          class="text-magenta-cta underline"
          target="_blank"
          title="Aide DORA - ouverture dans une nouvelle fenêtre"
          rel="noopener noreferrer"
          href={`${URL_HELP_SITE}category/inscription-et-gestion-du-compte-ha8m5b/`}
        >
          Besoin d’aide&#8239;? Contactez-nous
        </a>
      {/if}
      &nbsp;
      <a
        class="text-magenta-cta underline"
        target="_blank"
        title="Qu’est-ce que ProConnect&#8239;? nouvelle fenêtre"
        rel="noopener noreferrer"
        href={PROCONNECT_MORE_INFO_URL}
      >
        Qu'est que ProConnect&#8239;?
      </a>
    </div>
  {/if}
</div>
