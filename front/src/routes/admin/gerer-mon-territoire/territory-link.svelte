<script lang="ts">
  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import Spinner from "$lib/components/display/spinner.svelte";

  interface Props {
    label: string;
    to: string;
    openLinkInNewTab?: boolean;
    /** Nombre de structures concernées, affiché sous forme de badge suivant le libellé */
    count?: number;
    loading?: boolean;
  }

  let {
    label,
    to,
    openLinkInNewTab = false,
    count,
    loading = false,
  }: Props = $props();

  const hasCounter = $derived(count !== undefined || loading);
</script>

<a
  href={to}
  target={openLinkInNewTab ? "_blank" : null}
  title={openLinkInNewTab ? "Ouverture dans une nouvelle fenêtre" : null}
  rel={openLinkInNewTab ? "noopener nofollow" : null}
  class="text-f16 text-magenta-cta gap-s8 group inline-flex items-center font-bold"
>
  <span class="group-hover:underline">
    {label}{#if openLinkInNewTab}<ExternalLinkIcon />{/if}
  </span>

  {#if hasCounter}
    <span
      class="bg-blue-information text-service-blue-info px-s8 text-f14 inline-flex h-[22px] min-w-[26px] items-center justify-center rounded-full font-normal"
    >
      {#if loading}
        <Spinner size="12px" colorClass="border-gray-text-alt" />
      {:else}
        {count}
      {/if}
    </span>
  {/if}
</a>
