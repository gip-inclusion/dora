<script>
  import { validate } from "$lib/validation.js";
  import { serviceSchema } from "$lib/schemas/service.js";

  import Notice from "$lib/components/notice.svelte";

  export let service, servicesOptions;

  let validation;
  $: validation =
    service &&
    validate(service, serviceSchema, {
      noScroll: true,
      showErrors: false,
      extraData: servicesOptions,
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
