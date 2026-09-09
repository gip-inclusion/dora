<script lang="ts">
  import ExternalLinkIcon from "$lib/components/display/external-link-icon.svelte";
  import Spinner from "$lib/components/display/spinner.svelte";

  interface Props {
    label: string;
    to: string;
    otherTab?: boolean;
    /** Nombre de structures concernées, affiché sous forme de badge suivant le libellé */
    count?: number;
    loading?: boolean;
  }

  let { label, to, otherTab = false, count, loading = false }: Props = $props();

  const hasCounter = $derived(count !== undefined || loading);
</script>

<a
  href={to}
  target={otherTab ? "_blank" : null}
  title={otherTab ? "Ouverture dans une nouvelle fenêtre" : null}
  rel={otherTab ? "noopener nofollow" : null}
  class="text-f16 text-magenta-cta gap-s8 inline-flex items-center font-bold hover:underline"
>
  <span>
    {label}{#if otherTab}<ExternalLinkIcon />{/if}
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
