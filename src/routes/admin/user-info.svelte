<script lang="ts">
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
        📞 <a href="tel:{user.phoneNumber}">{user.phoneNumber}</a>
        <br />
      {/if}
    </div>
  {/if}
{/if}
