<script lang="ts">
  import Notice from "$lib/components/display/notice.svelte";
  import { validate } from "$lib/validation/validation";
  import {
    inclusionNumeriqueSchema,
    serviceSchema,
  } from "$lib/validation/schemas/service";
  import { onMount } from "svelte";

  let { service, servicesOptions } = $props();

  let invalidFields: string[] = $state([]);
  let numErrors = $state();

  onMount(() => {
    const schema = service.useInclusionNumeriqueScheme
      ? inclusionNumeriqueSchema
      : serviceSchema;
    const validation = validate(service, schema, {
      noScroll: true,
      showErrors: false,
      servicesOptions,
    });
    invalidFields = validation?.errorFields;
    numErrors = invalidFields.length;
  });
</script>

{#if invalidFields.length}
  <Notice
    title={`Information${numErrors > 1 ? "s" : ""} requise${
      numErrors > 1 ? "s" : ""
    } pour publier`}
    type="warning"
  >
    <p class="text-f14 first-letter:capitalize">
      {invalidFields.join(", ")}.
    </p>
  </Notice>
{/if}
