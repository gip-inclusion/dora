<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import SyncIcon from "$lib/assets/icons/ico-sync.svelte";

  interface Props {
    onclick: () => void;
    label: string;
    extraClass?: string;
  }

  const { onclick, label, extraClass = "" }: Props = $props();
</script>

<Button
  {onclick}
  icon={SyncIcon}
  noBackground
  small
  noPadding
  label={`Utiliser ${label} de la structure`}
  {extraClass}
/>
