<script lang="ts">
  import { orientationState } from "./state.svelte";
  import type { OrientationStats } from "$lib/types";

  interface Props {
    stats: OrientationStats;
  }

  const { stats }: Props = $props();
</script>

<p>
  {#if orientationState.selectedType === "sent"}
    <b
      >{stats.totalSentPending > 1
        ? `${stats.totalSentPending} demandes`
        : `${stats.totalSentPending} demande`}

      en cours</b
    >
    / {stats.totalSent > 1
      ? `${stats.totalSent} envoyées`
      : `${stats.totalSent} envoyée`}
  {:else}
    <b
      >{stats.totalReceivedPending > 1
        ? `${stats.totalReceivedPending} demandes`
        : `${stats.totalReceivedPending} demande`}
      à traiter / {stats.totalReceived > 1
        ? `${stats.totalReceived} reçues`
        : `${stats.totalReceived} reçue`}
    </b>
  {/if}
</p>
