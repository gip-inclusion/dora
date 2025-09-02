<script lang="ts">
  import CheckboxesField from "./checkboxes-field.svelte";

  interface Props {
    id: string;
    value?: boolean;
    disabled?: boolean;
    readonly?: boolean;
    // Spécifiques
    label: string;
    // Proxy vers le FieldWrapper
    description?: string;
    hidden?: boolean;
    hideLabel?: boolean;
    vertical?: boolean;
  }

  let {
    id,
    value = $bindable(false),
    disabled = false,
    readonly = false,
    label,
    description = "",
    hidden = false,
    hideLabel = false,
    vertical = false,
  }: Props = $props();

  const choices = [{ value: "true", label }];

  let checkboxesFieldValue = $state(value ? ["true"] : []);

  $effect(() => {
    value = checkboxesFieldValue.length > 0;
  });
</script>

<CheckboxesField
  {id}
  bind:value={checkboxesFieldValue}
  {choices}
  {disabled}
  {readonly}
  {description}
  {hidden}
  {hideLabel}
  {vertical}
/>
