<script lang="ts">
  import type { PageData } from "./$types";
  import FormWrapper from "./form-wrapper.svelte";

  export let data: PageData;
</script>

<FormWrapper servicesOptions={data.servicesOptions} source={data.source} />
