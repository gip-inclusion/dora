<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import FieldsAddress from "./fields-address.svelte";
  import type { Service, ServicesOptions, Structure } from "$lib/types";
  import { moveToTheEnd } from "$lib/utils/misc";

  export let servicesOptions: ServicesOptions, service: Service;
  export let structure: Structure | undefined = undefined;
</script>

<FieldSet title="Accueil">
  <CheckboxesField
    id="locationKinds"
    bind:value={service.locationKinds}
    choices={moveToTheEnd(servicesOptions.locationKinds, "value", "a-distance")}
  />

  {#if service.locationKinds.includes("a-distance")}
    <BasicInputField
      type="url"
      id="remoteUrl"
      placeholder="https://"
      bind:value={service.remoteUrl}
    />
  {/if}

  {#if service.locationKinds.includes("en-presentiel")}
    <FieldsAddress bind:entity={service} parent={structure} />
  {/if}
</FieldSet>
