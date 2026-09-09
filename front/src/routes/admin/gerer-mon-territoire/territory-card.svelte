<script lang="ts">
  import type { Snippet } from "svelte";

  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  import LinkButton from "$lib/components/display/link-button.svelte";

  interface Props {
    title: string;
    illustration: string;
    /** L'illustration et le bouton d'action pointent vers la même destination */
    to: string;
    openLinkInNewTab?: boolean;
    ctaLabel: string;
    links: Snippet;
  }

  let {
    title,
    illustration,
    to,
    openLinkInNewTab = false,
    ctaLabel,
    links,
  }: Props = $props();
</script>

<div class="gap-s16 flex h-full flex-col">
  <h2 class="mb-s0 text-france-blue text-f20 lg:text-f22">{title}</h2>

  <a
    href={to}
    target={openLinkInNewTab ? "_blank" : null}
    title={openLinkInNewTab ? "Ouverture dans une nouvelle fenêtre" : null}
    rel={openLinkInNewTab ? "noopener nofollow" : null}
    class="focus:shadow-focus rounded-lg"
  >
    <img src={illustration} alt="" class="w-full" />
  </a>

  <div class="gap-s12 mb-s8 flex flex-col items-start">
    {@render links()}
  </div>

  <div class="mt-auto">
    <LinkButton
      label={ctaLabel}
      {to}
      otherTab={openLinkInNewTab}
      nofollow={openLinkInNewTab}
      wFull
      canWrap
      icon={openLinkInNewTab ? ExternalLinkLineSystem : undefined}
      iconOnRight
    />
  </div>
</div>
