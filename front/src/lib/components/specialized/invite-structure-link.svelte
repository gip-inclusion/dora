<script lang="ts">
  import LinkButton from "../display/link-button.svelte";

  interface Props {
    wFull?: boolean;
  }

  let { wFull = false }: Props = $props();
</script>

<LinkButton
  label="Inviter une structure partenaire"
  secondary
  otherTab
  {wFull}
  to="https://tally.so/r/nGegBe"
/>
