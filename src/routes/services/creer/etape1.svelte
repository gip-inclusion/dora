<script>
  import { service } from "./_creation-store.js";
  import { serviceOptions } from "./_services-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, null, "etape2");
  }
</script>

{#if $serviceOptions}
  <form on:submit|preventDefault={handleSubmit}>
    <FieldSet title="Présentez votre offre de service">
      <Field
        type="text"
        field={$serviceOptions.name}
        bind:value={$service.name} />
      <Field
        type="text"
        field={$serviceOptions.shortDesc}
        bind:value={$service.shortDesc} />
      <Field
        type="richtext"
        field={$serviceOptions.fullDesc}
        bind:value={$service.fullDesc} />
    </FieldSet>

    <FieldSet title="Typologie de l‘offre">
      <Field
        type="checkboxes"
        field={$serviceOptions.kinds}
        bind:value={$service.kinds} />
      <Field
        type="multiselect"
        field={$serviceOptions.categories}
        bind:value={$service.categories}
        bind:selectedItems={$service._categoriesItems}
        placeholder="Choissisez une catégorie" />
      <Field
        type="multiselect"
        field={$serviceOptions.subcategories}
        bind:value={$service.subcategories}
        bind:selectedItems={$service._subcategoriesItems}
        placeholder="Précisez la catégorie" />
      <Field
        type="toggle"
        field={$serviceOptions.isCommonLaw}
        bind:value={$service.isCommonLaw} />
    </FieldSet>

    <NavButtons withForward />
  </form>
{/if}
