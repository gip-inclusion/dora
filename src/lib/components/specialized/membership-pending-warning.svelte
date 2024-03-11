<script lang="ts">
  import { userInfo } from "$lib/utils/auth";
</script>

{#if $userInfo.pendingStructures.length === 1}
  Le temps que votre adhésion à la structure “{$userInfo.pendingStructures[0]
    .name}” soit validée, vous ne pouvez pas visualiser ces informations.
{:else}
  Le temps que vos demandes d’adhésion soient validées, vous ne pouvez pas
  visualiser ces informations.
{/if}
