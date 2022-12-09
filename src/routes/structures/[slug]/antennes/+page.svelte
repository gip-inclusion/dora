<script lang="ts">
  import { structure } from "../store";
  import List from "./list.svelte";
</script>

<List
  branches={$structure.branches}
  structure={$structure}
  total={$structure.branches.length}
/>
