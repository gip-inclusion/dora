<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
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
        placeholder="Sélectionnez votre structure" />
    </FieldSet>

    <FieldSet title="Présentez votre offre de service">
      <ModelField
        type="text"
        field={$serviceOptions.name}
        bind:value={$serviceCache.name} />
      <ModelField
        type="text"
        field={$serviceOptions.shortDesc}
        bind:value={$serviceCache.shortDesc}>
        <FieldHelp title="Présentation résumée">
          <p>
            Lors de l’affichage de la solution, nous aurons besoin de voir une
            présentation brève de ce que propose votre solution avec seulement
            les éléments principaux.
          </p>
          <p>
            <strong>Par exemple :</strong> Faciliter vos déplacements en cas de
            recherche d'emploi (entretien d'embauche, concours public). Voir
            <a href="#" class="underline text-information">lorem ipsum</a>
          </p>
        </FieldHelp>
      </ModelField>
      <ModelField
        type="richtext"
        field={$serviceOptions.fullDesc}
        bind:value={$serviceCache.fullDesc} />
    </FieldSet>

    <FieldSet title="Typologie de l‘offre">
      <ModelField
        type="checkboxes"
        field={$serviceOptions.kinds}
        bind:value={$serviceCache.kinds}
        description="Quel type de service proposez-vous ? " />
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
        placeholder="Précisez la catégorie">
        <FieldHelp title="Catégorisation">
          Pour permettre à nos utilisateurs de trouver facilement la solution
          que vous proposez. Il est nécessaire de classer les offres par
          catégorie et de préciser le type d’offre.
        </FieldHelp>
      </ModelField>
      <ModelField
        type="toggle"
        field={$serviceOptions.isCommonLaw}
        bind:value={$serviceCache.isCommonLaw}
        description="Il s’agit d’un service de Droit commun - mobilisé équitablement sur l’ensemble du territoire ?" />
    </FieldSet>

    <NavButtons withForward />
  </form>
{/if}
