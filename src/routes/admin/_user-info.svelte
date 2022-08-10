<script>
  import Date from "$lib/components/date.svelte";
  import EmailLine from "./_email-line.svelte";

  import WebSearchLink from "./_web-search-link.svelte";

  export let user, structure;
</script>

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
  {user.newsletter ? "✅" : "❌"}
  <br />
  inscription: <Date date={user.dateJoined} />
</div>
