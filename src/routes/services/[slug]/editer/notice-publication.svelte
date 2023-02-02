<script lang="ts">
  import Notice from "$lib/components/display/notice.svelte";
  import { currentSchema, validate } from "$lib/validation/validation";
  import { onMount } from "svelte";

  export let service, servicesOptions;

  let invalidFields: string[] = [];
  let numErrors;

  onMount(() => {
    const validation = validate(service, $currentSchema, {
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
