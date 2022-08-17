<script lang="ts">
  import Date from "$lib/components/date.svelte";

  import Label from "$lib/components/label.svelte";
  import type { ModerationStatus } from "$lib/enums";

  export let status: ModerationStatus;
  export let date: string;
</script>

{#if status === "NEED_INITIAL_MODERATION"}
  <Label label="Première modération nécessaire" bold error />
{:else if status === "NEED_NEW_MODERATION"}
  <Label label="Nouvelle modération nécessaire" bold error />
{:else if status === "IN_PROGRESS"}
  <Label bold wait>
    En cours depuis le <Date {date} />
  </Label>
{:else if status === "VALIDATED"}
  <Label label="Validé" bold success />
{/if}
