<script lang="ts">
  import Label from "$lib/components/display/label.svelte";
  import DateLabel from "$lib/components/utilities/date-label.svelte";
  import type { ModerationStatus } from "$lib/types";

  export let status: ModerationStatus;
  export let date: string;
</script>

{#if status === "NEED_INITIAL_MODERATION"}
  <Label label="Première modération nécessaire" bold error />
{:else if status === "NEED_NEW_MODERATION"}
  <Label label="Nouvelle modération nécessaire" bold error />
{:else if status === "IN_PROGRESS"}
  <Label bold wait>
    En cours depuis le
    <DateLabel {date} />
  </Label>
{:else if status === "VALIDATED"}
  <Label label="Validé" bold success />
{:else}
  <Label label="Non spécifié" bold error />
{/if}
