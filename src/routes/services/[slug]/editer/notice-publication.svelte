<script lang="ts">
  import Notice from "$lib/components/display/notice.svelte";
  import { serviceSchema } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";

  export let service, servicesOptions;

  let validation;
  $: validation =
    service &&
    validate(service, serviceSchema, {
      noScroll: true,
      showErrors: false,
      servicesOptions,
    });

  let errors;
  $: errors = validation?.errorFields.length > 1;
</script>

{#if !validation?.valid}
  <Notice
    title={`Information${errors ? "s" : ""} requise${
      errors ? "s" : ""
    } pour publier`}
    type="warning"
  >
    <p class="text-f14 first-letter:capitalize">
      {validation?.errorFields.join(", ")}.
    </p>
  </Notice>
{/if}
