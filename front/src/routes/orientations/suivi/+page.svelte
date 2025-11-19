<script lang="ts">
  import ExportDisplay from "./export-display.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  import { orientationState, items } from "./state.svelte.js";
</script>

<EnsureLoggedIn>
  <ExportDisplay
    stats={{ pending: 0, total: 0 }}
    type={orientationState.selectedType}
    title={items.filter((item) => item.id === orientationState.selectedType)[0]
      .name}
  />
</EnsureLoggedIn>
