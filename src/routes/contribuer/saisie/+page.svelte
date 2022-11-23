<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let { servicesOptions, source } = data;
  import FormWrapper from "../form/_form-wrapper.svelte";
</script>

<svelte:head>
  <title>Contribuer | DORA</title>
</svelte:head>

<FormWrapper {servicesOptions} {source} />
