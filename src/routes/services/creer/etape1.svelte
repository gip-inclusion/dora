<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, null, "etape2");
  }
</script>

{#if $serviceOptions}
  <form on:submit|preventDefault={handleSubmit}>
    <FieldSet title="">
      <ModelField
        type="select"
        field={$serviceOptions.structure}
        bind:value={$serviceCache.structure}
        bind:selectedItem={$serviceCache._structure}
        placeholder="Précisez la catégorie" />
    </FieldSet>

    <FieldSet title="Présentez votre offre de service">
      <ModelField
        type="text"
        field={$serviceOptions.name}
        bind:value={$serviceCache.name} />
      <ModelField
        type="text"
        field={$serviceOptions.shortDesc}
        bind:value={$serviceCache.shortDesc} />
      <ModelField
        type="richtext"
        field={$serviceOptions.fullDesc}
        bind:value={$serviceCache.fullDesc} />
    </FieldSet>

    <FieldSet title="Typologie de l‘offre">
      <ModelField
        type="checkboxes"
        field={$serviceOptions.kinds}
        bind:value={$serviceCache.kinds} />
      <ModelField
        type="multiselect"
        field={$serviceOptions.categories}
        bind:value={$serviceCache.categories}
        bind:selectedItem={$serviceCache._categoriesItems}
        placeholder="Choisissez une catégorie" />
      <ModelField
        type="multiselect"
        field={$serviceOptions.subcategories}
        bind:value={$serviceCache.subcategories}
        bind:selectedItem={$serviceCache._subcategoriesItems}
        placeholder="Précisez la catégorie" />
      <ModelField
        type="toggle"
        field={$serviceOptions.isCommonLaw}
        bind:value={$serviceCache.isCommonLaw} />
    </FieldSet>

    <NavButtons withForward />
  </form>
{/if}
