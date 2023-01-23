<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import BooleanRadioButtonsField from "$lib/components/inputs/boolean-radio-buttons-field.svelte";
  import type { Service } from "$lib/types";

  export let service: Service;
</script>

<FieldSet title="Contact du référent">
  <div slot="help">
    <p class="text-f14">
      Coordonnées de la personne responsable de la réception et du traitement
      des demandes d’orientation. À défaut, renseignez le courriel et le numéro
      de téléphone de votre structure.
    </p>
    <p class="text-f14">
      Par défaut, ces informations sont disponibles uniquement aux
      accompagnateurs qui ont un compte DORA. En cochant la case « Rendre
      public », les informations seront rendues disponibles à tous les visiteurs
      du site.
    </p>
  </div>
  <BasicInputField
    id="contactName"
    placeholder="Prénom et nom"
    bind:value={service.contactName}
  />

  <BasicInputField
    id="contactPhone"
    type="tel"
    placeholder="00 00 00 00 00"
    bind:value={service.contactPhone}
  />

  <BasicInputField
    id="contactEmail"
    type="email"
    placeholder="nom@exemple.org"
    bind:value={service.contactEmail}
  />

  <BooleanRadioButtonsField
    id="isContactInfoPublic"
    bind:value={service.isContactInfoPublic}
    yesLabel="OUI – visibles pour tout visiteur du site DORA"
    noLabel="NON – visibles uniquement par les professionnels inscrits sur DORA "
  />
</FieldSet>
