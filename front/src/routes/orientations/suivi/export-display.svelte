<script lang="ts">
  import NoOrientationsCard from "./no-orientations-card.svelte";

  import type { OrientationType } from "./state.svelte.js";

  interface Props {
    type: OrientationType;
    title: string;
    stats: { pending: number; total: number };
  }

  const { type, title, stats }: Props = $props();
</script>

<div>
  <h2>{title}</h2>
  {#if type === "sent"}
    <p><b>{stats.pending} demandes en cours</b> / {stats.total} envoyées</p>
  {:else}
    <p><b>{stats.pending} demandes à traiter</b> / {stats.total} reçues</p>
  {/if}
  {#if type === "received" && stats.total === 0}
    <NoOrientationsCard
      title="Aucune demande d'orientation reçue pour le moment"
      text="Assurez-vous d'avoir activé le formulaire DORA sur vos services. Pour
      augmenter votre visibilité, partagez le lien de votre structure avec vos
      partenaires afin qu'ils puissent orienter leurs bénéficiaires vers vos
      dispositifs via DORA."
      ><button class="text-magenta-cta">Paser en revue mes services</button>
      <button class="text-magenta-cta">Copier le lien de ma structure</button
      ></NoOrientationsCard
    >
  {:else if type === "sent" && stats.total === 0}
    <NoOrientationsCard
      title="Vous n'avez pas encore réalisé d'orientations"
      text="Besoin d'orienter des bénéficiaires vers des dispositifs adaptés ?
      Commencez par identifier les services disponibles selon leurs besoins et
      votre territoire."
    >
      <a href="recherche" class="text-magenta-cta">Rechercher par mots-clé</a>
      <a href="recherche" class="text-magenta-cta"
        >Rechercher par lieu et besoins</a
      ></NoOrientationsCard
    >
  {/if}
</div>
