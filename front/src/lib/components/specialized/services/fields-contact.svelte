<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import type { Service } from "$lib/types";

  interface Props {
    service: Service;
  }

  let { service = $bindable() }: Props = $props();
</script>

<FieldSet title="Contact du référent">
  {#snippet help()}
    <div>
      <p class="text-f14">
        Coordonnées de la personne responsable de la réception et du traitement
        des demandes d’orientation. À défaut, renseignez le courriel et le
        numéro de téléphone de votre structure.
      </p>
      <p class="text-f14">
        Par défaut, ces informations sont disponibles uniquement aux
        accompagnateurs qui ont un compte DORA. En cochant la case « Rendre
        public », les informations seront rendues disponibles à tous les
        visiteurs du site.
      </p>
    </div>
  {/snippet}
  <BasicInputField
    id="contactName"
    bind:value={service.contactName}
    description="Personne (prénom et nom) ou département/service interne (nom) en charge de la réception et du traitement des orientations, pour ce service."
  />

  <BasicInputField
    id="contactPhone"
    type="tel"
    description="Format attendu : 4 à 10 caractères alphanumériques (sans l'indicatif pays). Par exemple : 0123456789."
    bind:value={service.contactPhone}
  />

  <BasicInputField
    id="contactEmail"
    type="email"
    description="Format attendu&nbsp;: nom@domaine.fr"
    bind:value={service.contactEmail}
  />

  <BooleanRadioButtonsField
    id="isContactInfoPublic"
    bind:value={service.isContactInfoPublic}
    yesLabel="OUI – visibles publiquement"
    noLabel="NON – visibles par les acteurs de l’insertion"
  />
</FieldSet>
