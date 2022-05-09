<script>
  import Notice from "$lib/components/notice.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import { userInfo } from "$lib/auth";

  export let structure;
</script>

<Notice title="Vous êtes le gestionnaire de cette structure ?">
  <p class="mb-s4 text-f14">
    Créez votre compte sur DORA. Vous pourrez ensuite mettre à jour les services
    de votre structure.
  </p>

  <div slot="button">
    {#if $userInfo}
      <LinkButton
        label="Demander l’accès"
        to="https://itou.typeform.com/doracontactsupp"
        otherTab
        nofollowsmall
        secondary
        small
      />
    {:else}
      <LinkButton
        label="Demander l’accès"
        to="/auth/inscription?siret={structure.siret}"
        otherTab
        nofollow
        small
        secondary
      />
    {/if}
  </div>
</Notice>
