<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import type {
    inclusionNumeriqueSchema,
    serviceSchema,
  } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";
  import { onMount } from "svelte";

  export let service, servicesOptions;
  export let schema: typeof serviceSchema | typeof inclusionNumeriqueSchema;

  let invalidFields: string[] = [];
  let numErrors;

  onMount(() => {
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
  <CenteredGrid>
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
  </CenteredGrid>
{/if}
