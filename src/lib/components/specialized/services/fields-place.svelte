<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/inputs/checkboxes-field.svelte";
  import FieldsAddress from "$lib/components/specialized/services/fields-address.svelte";
  import type { Service, ServicesOptions, Structure } from "$lib/types";
  import { moveToTheEnd } from "$lib/utils/misc";
  import type { Schema } from "$lib/validation/schemas/utils";

  export let schema: Schema;
  export let servicesOptions: ServicesOptions, service: Service;
  export let structure: Structure | undefined = undefined;
</script>

<FieldSet title="Accueil">
  <CheckboxesField
    id="locationKinds"
    schema={schema.locationKinds}
    bind:value={service.locationKinds}
    choices={moveToTheEnd(servicesOptions.locationKinds, "value", "a-distance")}
  />

  {#if service.locationKinds.includes("a-distance")}
    <BasicInputField
      type="url"
      id="remoteUrl"
      schema={schema.remoteUrl}
      placeholder="https://"
      bind:value={service.remoteUrl}
    />
  {/if}

  {#if service.locationKinds.includes("en-presentiel")}
    <FieldsAddress bind:entity={service} parent={structure} {schema} />
  {/if}
</FieldSet>
