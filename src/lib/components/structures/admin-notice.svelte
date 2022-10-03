<script>
  import Notice from "$lib/components/notice.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  export let structure;
</script>

<Notice title="Vous gérez cette structure ?">
  <div slot="button">
    <LinkButton
      label="Demander l’accès"
      to="/auth/rattachement?siret={structure.siret}"
      otherTab
      nofollow
      secondary
      small
    />
  </div>
</Notice>
