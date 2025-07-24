<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import Notice from "$lib/components/display/notice.svelte";

  let { structure } = $props();
</script>

<Notice title="Vous gérez cette structure ?">
  {#snippet button()}
    <div>
      <LinkButton
        label="Demander l’accès"
        to="/auth/rattachement?siret={structure.siret}"
        otherTab
        secondary
        small
      />
    </div>
  {/snippet}
</Notice>
