<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import Info from "./_info.svelte";

  import CustomLayout from "./_custom-layout.svelte";
  import NavButtons from "./_nav.svelte";
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $serviceOptions}
      <FieldSet title="">
        <ModelField
          type="select"
          field={$serviceOptions.structure}
          bind:value={$serviceCache.structure}
          bind:selectedItem={$serviceCache._structure}
          placeholder="Sélectionnez votre structure" />
      </FieldSet>

      <FieldSet title="Typologie de service">
        <Info title="Périmètre de test">
          Pour tester rapidement un maximum de leviers et itérer rapidement,
          l’équipe va se focaliser sur un périmètre d’expérimentation réduit en
          matière d’offre. Thématiques d’offres ciblées : <strong
            >mobilité, <strong>garde d’enfant</strong> et
            <strong>hébergement/logement</strong>.
          </strong></Info>

        <ModelField
          type="multiselect"
          field={$serviceOptions.categories}
          bind:value={$serviceCache.categories}
          bind:selectedItem={$serviceCache._categoriesItems}
          placeholder="Choisissez la catégorie principale" />
        <ModelField
          type="multiselect"
          field={$serviceOptions.subcategories}
          bind:value={$serviceCache.subcategories}
          bind:selectedItem={$serviceCache._subcategoriesItems}
          placeholder="Choisissez les sous-catégories">
          <FieldHelp slot="helptext" title="Catégorisation">
            Pour permettre à nos utilisateurs de trouver facilement la solution
            que vous proposez. Il est nécessaire de classer les offres par
            catégorie et de préciser le type d’offre.
          </FieldHelp>
        </ModelField>

        <ModelField
          type="checkboxes"
          field={$serviceOptions.kinds}
          bind:value={$serviceCache.kinds}
          description="Quel type de service proposez-vous ? " />

        <ModelField
          type="toggle"
          label="Droit commun"
          field={$serviceOptions.isCommonLaw}
          bind:value={$serviceCache.isCommonLaw}
          description="Il s’agit d’un service de Droit commun - mobilisé équitablement sur l’ensemble du territoire ?" />
      </FieldSet>

      <FieldSet title="Présentez votre service">
        <ModelField
          label="Nom de l’offre"
          type="text"
          placeholder="Ex. Aide aux frais liés à…"
          field={$serviceOptions.name}
          bind:value={$serviceCache.name} />
        <ModelField
          description="280 caractères maximum"
          placeholder="Décrivez brièvement votre service"
          type="textarea"
          field={$serviceOptions.shortDesc}
          bind:value={$serviceCache.shortDesc}>
          <FieldHelp slot="helptext" title="Résumé">
            <p>
              Lors de l’affichage du service, nous aurons besoin de voir une
              présentation brève de ce que propose votre service avec seulement
              les éléments principaux.
            </p>
            <p>
              <strong>Par exemple :</strong> Faciliter vos déplacements en cas
              de recherche d'emploi (entretien d'embauche, concours public).
              Voir
              <a href="" class="underline text-information">lorem ipsum</a>
            </p>
          </FieldHelp>
        </ModelField>
        <ModelField
          label="Descriptif complet du service"
          placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre service et ses spécificités."
          type="richtext"
          field={$serviceOptions.fullDesc}
          bind:value={$serviceCache.fullDesc} />
      </FieldSet>
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="navbar">
    <NavButtons withForward forwardlink="etape2" />
  </svelte:fragment>
</CustomLayout>
