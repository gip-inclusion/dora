<script lang="ts">
  import NoOrientationsCard from "./no-orientations-card.svelte";

  import type { OrientationType } from "./state.svelte.js";
  import type { OrientationStats } from "$lib/types";

  interface Props {
    type: OrientationType;
    title: string;
    stats: OrientationStats;
  }

  const { type, title, stats }: Props = $props();

  const showNoOrientationsCard =
    (type === "sent" && stats.totalSent === 0) ||
    (type === "received" && stats.totalReceivedPending === 0);
</script>

<div>
  <h2>{title}</h2>
  {#if type === "sent"}
    <p>
      <b>{stats.totalSentPending} demandes en cours</b> / {stats.totalSent} envoyées
    </p>
  {:else}
    <p>
      <b>{stats.totalReceivedPending} demandes à traiter</b> / {stats.totalReceived}
      reçues
    </p>
  {/if}
  {#if showNoOrientationsCard}
    <NoOrientationsCard {type} />
  {/if}
</div>
