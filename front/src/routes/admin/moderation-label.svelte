<script lang="ts">
  import Label from "$lib/components/display/label.svelte";
  import DateLabel from "$lib/components/display/date-label.svelte";
  import type { ModerationStatus } from "$lib/types";

  interface Props {
    status: ModerationStatus;
    date: string;
  }

  let { status, date }: Props = $props();
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
