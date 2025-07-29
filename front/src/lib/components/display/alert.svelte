<script lang="ts">
  import { alertIcon } from "$lib/icons";

  interface Props {
    id: string;
    label: string;
  }

  let { id, label }: Props = $props();
</script>

<div {id} class="pt-s4 text-f12 text-error flex flex-row items-center">
  <div class="mr-s8 h-s16 w-s16 fill-current">
    {@html alertIcon}
  </div>
  {label}
</div>
