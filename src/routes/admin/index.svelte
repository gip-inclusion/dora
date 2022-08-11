<script>
  import LinkButton from "$lib/components/link-button.svelte";
</script>

<div class="flex w-1/3 flex-col gap-s8 lg:flex-row">
  <LinkButton label="Structures" to="/admin/structures" secondary small />
  <LinkButton label="Services" to="/admin/services" secondary small />
  <LinkButton label="Contributions" to="/admin/contributions" secondary small />
</div>
