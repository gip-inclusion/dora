<script lang="ts">
  import DateLabel from "$lib/components/display/date-label.svelte";
  import EmailLine from "./email-line.svelte";
  import GoogleSearchLink from "./google-search-link.svelte";
  import LinkedinSearchLink from "./linkedin-search-link.svelte";

  export let user, structure;
</script>

{#if user}
  {#if user.email === "dora-bot@dora.beta.gouv.fr"}
    <strong>L’équipe DORA</strong>
  {:else}
    <div>
      <strong>
        {user.firstName}
        {user.lastName}
      </strong>

      <GoogleSearchLink
        searchString="{user.firstName} {user.lastName} {user.email} {structure.name}"
      />
      <LinkedinSearchLink
        searchString="{user.firstName} {user.lastName}"
        kind={"people"}
      />

      <EmailLine email={user.email} />

      {#if user.phoneNumber}
        📞 {user.phoneNumber}
        <br />
      {/if}
      valide: {user.isValid ? "✅" : "❌"}<br />sur Inclusion Connect: {user.isOnIc
        ? "✅"
        : "❌"}
      <br />
      inscription: <DateLabel date={user.dateJoined} />
    </div>
  {/if}
{/if}
