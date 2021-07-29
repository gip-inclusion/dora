<script>
  import { service } from "./_creation-store.js";
  import { serviceOptions } from "./_services-store.js";

  import Field from "$lib/components/forms/field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, null, "etape2");
  }
</script>

{#if $serviceOptions && service}
  <form on:submit|preventDefault={handleSubmit}>
    <h2 class="w-full mt-20 mb-4 text-xl font-bold ">
      Présentez votre offre de service
    </h2>
    <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-gray-01">
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
    </div>

    <h2 class="w-full mt-20 mb-4 text-xl font-bold ">Typologie de l‘offre</h2>
    <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-gray-01">
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
    </div>

    <NavButtons withForward />
  </form>
{/if}
