<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
</script>

<CenteredGrid>
  <div class="flex w-1/3 flex-col gap-s8 lg:flex-row">
    <LinkButton label="Structures" to="/admin/structures" secondary small />
    <LinkButton label="Services" to="/admin/services" secondary small />
    <LinkButton
      label="Contributions"
      to="/admin/contributions"
      secondary
      small
    />
    <LinkButton label="Moderation" to="/admin/moderation" secondary small />
  </div>
</CenteredGrid>
