<script>
  import { validate } from "$lib/validation.js";
  import schema, { fields, fieldsRequired } from "$lib/schemas/service.js";

  import Notice from "$lib/components/notice.svelte";
  import { formatSchema } from "$lib/schemas/utils";

  export let service;

  const serviceSchema = formatSchema(
    schema,
    fields.service,
    fieldsRequired.service
  );

  let validation;
  $: validation =
    service &&
    validate(service, serviceSchema, { noScroll: true, showErrors: false });

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
