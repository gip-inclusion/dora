<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import UseStructureInfoButton from "./use-structure-info-button.svelte";

  import type { Service } from "$lib/types";
  import { currentSchema } from "$lib/validation/validation";
  import { formatPhoneNumber } from "$lib/utils/misc";

  interface Props {
    service: Service;
  }

  let { service = $bindable() }: Props = $props();
</script>

<FieldSet title="Contact du service">
  {#snippet help()}
    <div>
      <p class="text-f14">
        Coordonnées de la personne responsable de la réception et du traitement
        des demandes d’orientation. À défaut, vous pouvez renseigner le courriel
        et le numéro de téléphone de votre structure.
      </p>
      <p class="text-f14">
        Par défaut, ces informations sont disponibles uniquement aux
        accompagnateurs qui ont un compte DORA. En cochant la case «&nbsp;Rendre
        les informations de contact publiques&nbsp;», les informations seront
        rendues disponibles à tous les visiteurs du site.
      </p>
    </div>
  {/snippet}
  <BasicInputField
    id="contactName"
    bind:value={service.contactName}
    descriptionText="Personne ou service en charge des orientations."
  />
  <div class="flex flex-col">
    {#if service.structureInfo.phone}
      <div class="pl-s4 lg:w-2/3 lg:self-end">
        <UseStructureInfoButton
          onclick={() =>
            (service = {
              ...service,
              contactPhone: formatPhoneNumber(service.structureInfo.phone),
            })}
          label="le téléphone"
        />
      </div>
    {/if}
    <BasicInputField
      id="contactPhone"
      type="tel"
      descriptionText="Format attendu : 4 à 10 caractères alphanumériques (sans l'indicatif pays). Par exemple : 0123456789."
      bind:value={service.contactPhone}
    />
  </div>
  <div class="flex flex-col">
    {#if service.structureInfo.email}
      <div class="pl-s4 lg:w-2/3 lg:self-end">
        <UseStructureInfoButton
          onclick={() => (service.contactEmail = service.structureInfo.email)}
          label="le courriel"
        />
      </div>
    {/if}
    <BasicInputField
      id="contactEmail"
      type="email"
      descriptionText="Format attendu&nbsp;: nom@domaine.fr"
      bind:value={service.contactEmail}
    />
  </div>

  {#if $currentSchema && "isContactInfoPublic" in $currentSchema}
    <BooleanRadioButtonsField
      id="isContactInfoPublic"
      bind:value={service.isContactInfoPublic}
      yesLabel="OUI – visibles publiquement"
      noLabel="NON – visibles par les professionnels de l’insertion"
    />
  {/if}
</FieldSet>
