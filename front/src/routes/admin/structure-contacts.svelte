<script lang="ts">
  import EmailLine from "./email-line.svelte";
  import InfoLine from "./info-line.svelte";
  import UserInfo from "./user-info.svelte";

  export let structure;
  const administrators = structure.members.filter((member) => member.isAdmin);
</script>

{#if structure.phone || structure.email}
  <h1>Informations de contact géneriques</h1>
  <InfoLine condition={structure.phone || structure.email}>
    {#if structure.phone}📞 {structure.phone}{/if}
    {#if structure.email}<EmailLine email={structure.email} />{/if}
  </InfoLine>
{/if}

{#if structure.creator || structure.lastEditor}
  <h1>Historique</h1>
  {#if structure.creator}
    <InfoLine>
      structure créée par :
      <UserInfo user={structure.creator} {structure} />
    </InfoLine>
  {/if}
  {#if structure.lastEditor && structure.creator?.email !== structure.lastEditor?.email}
    <InfoLine>
      dernière modification par : <UserInfo
        user={structure.lastEditor}
        {structure}
      />
    </InfoLine>
  {/if}
{/if}

{#if administrators.length}
  <h1>administrateurs•trices</h1>
  {#each administrators as administrator}
    <InfoLine>
      <UserInfo user={administrator.user} {structure} />
    </InfoLine>
  {/each}
{/if}

<style lang="postcss">
  @reference "../../app.css";

  h1 {
  }
</style>
