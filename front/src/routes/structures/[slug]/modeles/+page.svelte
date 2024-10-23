<script lang="ts">
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import { structure } from "../store";
  import List from "./list.svelte";
</script>

<EnsureLoggedIn>
  <List
    models={$structure.models || []}
    structure={$structure}
    total={$structure.models.length}
    withEmptyNotice
  />
</EnsureLoggedIn>
