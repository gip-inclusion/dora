<script lang="ts">
  import Date from "$lib/components/utilities/date.svelte";
  import EmailLine from "./email-line.svelte";
  import WebSearchLink from "./web-search-link.svelte";

  export let user, structure;
</script>

{#if user}
  <div>
    <strong>
      {user.firstName}
      {user.lastName}
    </strong>

    <WebSearchLink
      searchString="{user.firstName} {user.lastName} {structure.name}"
    />

    <EmailLine email={user.email} />

    {#if user.phoneNumber}
      📞 {user.phoneNumber}
      <br />
    {/if}
    actif: {user.isActive ? "✅" : "❌"} valide: {user.isValid ? "✅" : "❌"} infolettre:
    {user.newsletter ? "✅" : "❌"} migré sur IC: {user.isOnIc ? "✅" : "❌"}
    <br />
    inscription: <Date date={user.dateJoined} />
  </div>
{/if}
