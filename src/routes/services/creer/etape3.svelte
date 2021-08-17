<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import CustomLayout from "./_custom-layout.svelte";

  import NavButtons from "./_nav.svelte";
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $serviceOptions}
      <FieldSet title="Modalités d'accès au service">
        <ModelField
          label="Comment mobiliser le service en tant que bénéficiaire ?"
          type="checkboxes"
          field={$serviceOptions.beneficiariesAccessModes}
          bind:value={$serviceCache.beneficiariesAccessModes}>
          <FieldHelp slot="helptext" title="Mobiliser le service">
            Quels sont les étapes à suivre pour pouvoir mobiliser le service ?
          </FieldHelp></ModelField>
        <ModelField
          visible={$serviceCache.beneficiariesAccessModes.includes("OT")}
          hideLabel
          placeholder="Merci de préciser la modalité"
          type="text"
          field={$serviceOptions.beneficiariesAccessModesOther}
          bind:value={$serviceCache.beneficiariesAccessModesOther} />
        <ModelField
          label="Comment orienter un bénéficiaire en tant qu’accompagnateur ?"
          type="checkboxes"
          field={$serviceOptions.coachOrientationModes}
          bind:value={$serviceCache.coachOrientationModes} />
        <ModelField
          visible={$serviceCache.coachOrientationModes.includes("OT")}
          hideLabel
          placeholder="Merci de préciser la modalité"
          type="text"
          field={$serviceOptions.coachOrientationModesOther}
          bind:value={$serviceCache.coachOrientationModesOther} />
        <ModelField
          placeholder="Choisissez ou ajoutez vos critères d’admission"
          type="multiselect"
          field={$serviceOptions.requirements}
          bind:value={$serviceCache.requirements}
          bind:selectedItem={$serviceCache._requirementsItems}>
          <FieldHelp slot="helptext" title="Accès au service">
            Quels sont les compétences, les diplômes qui limitent l’accès au
            service ?
          </FieldHelp></ModelField>
        <ModelField
          placeholder="Sélectionnez les justificatifs à fournir"
          type="multiselect"
          field={$serviceOptions.credentials}
          bind:value={$serviceCache.credentials}
          bind:selectedItem={$serviceCache._credentialsItems} />
        <ModelField
          type="files"
          field={$serviceOptions.forms}
          bind:value={$serviceCache.forms}>
          <FieldHelp slot="helptext" title="Justificatifs, documents">
            Mettre tous les documents maintenant, c’est permettre d’avoir des
            candidatures complètes avec moins d’aller/retour
          </FieldHelp></ModelField>
        <ModelField
          label="Le formulaire en ligne à compléter"
          placeholder="URL"
          type="url"
          field={$serviceOptions.onlineForms}
          bind:value={$serviceCache.onlineForms} />
      </FieldSet>
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="navbar">
    <NavButtons withBack withForward backlink="etape2" forwardlink="etape4" />
  </svelte:fragment>
</CustomLayout>
