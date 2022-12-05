<script lang="ts">
  import FormWrapper from "../form/form-wrapper.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<svelte:head>
  <title>Contribuer | DORA</title>
</svelte:head>

<FormWrapper servicesOptions={data.servicesOptions} source={data.source} />
