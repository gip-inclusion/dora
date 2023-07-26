<script lang="ts">
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import UploadField from "$lib/components/forms/fields/upload-field.svelte";
  import { formatFilePath } from "$lib/utils/file";
  import { orientation } from "../store";
  import { userInfo } from "$lib/utils/auth";
  import { onMount } from "svelte";
  import Accordion from "$lib/components/display/accordion.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";
  import { userPreferences } from "$lib/utils/preferences";

  export let service;
  export let credentials;

  let contactPrefOptions = [];

  if ($userInfo.structures?.length === 1) {
    $orientation.prescriberStructureSlug = $userInfo.structures[0].slug;
  } else {
    $orientation.prescriberStructureSlug = $userPreferences.visitedStructures
      .length
      ? $userInfo.structures.find(
          ({ slug }) => slug === $userPreferences.visitedStructures[0]
        )?.slug
      : $userInfo.structures[0].slug;
  }

  onMount(() => {
    contactPrefOptions = [
      { value: "TELEPHONE", label: "Téléphone" },
      { value: "EMAIL", label: "E-mail" },
      { value: "AUTRE", label: "Autre" },
    ];

    $orientation.referentLastName = $userInfo.lastName;
    $orientation.referentFirstName = $userInfo.firstName;
    $orientation.referentEmail = $userInfo.email;
  });
</script>

<div>
  {#if $userInfo.structures.length > 1}
    <div class="mb-s32">
      <SelectField
        id="prescriberStructureSlug"
        placeholder="Structure concernée"
        description="Vous faites partie de plusieurs structures, veuillez choisir celle qui sera mentionnée dans les e-mails envoyés aux partenaires."
        bind:value={$orientation.prescriberStructureSlug}
        vertical
        choices={$userInfo.structures.map((struct) => ({
          value: struct.slug,
          label: struct.name,
        }))}
      />
    </div>
  {/if}

  <Fieldset title="Conseiller ou conseillère référente" noTopPadding>
    <Notice type="info" title="Conseiller ou conseillère référente">
      <p class="mb-s0 text-f14 text-gray-text">
        Personne en charge de l’accompagnement et du suivi professionnel de la
        situation du bénéficiaire. Si ce n’est pas vous, veuillez modifier les
        informations ci-dessous.
      </p>
    </Notice>

    <div class="flex flex-row justify-items-stretch gap-s24">
      <div class="flex-1">
        <BasicInputField
          id="referentLastName"
          placeholder=""
          bind:value={$orientation.referentLastName}
          vertical
        />
      </div>
      <div class="flex-1">
        <BasicInputField
          id="referentFirstName"
          placeholder=""
          bind:value={$orientation.referentFirstName}
          vertical
        />
      </div>
    </div>
    <div class="flex flex-row justify-items-stretch gap-s24">
      <div class="flex-1">
        <BasicInputField
          id="referentPhone"
          type="tel"
          description="Format attendu&nbsp;: 0123456789"
          bind:value={$orientation.referentPhone}
          vertical
        />
      </div>
      <div class="flex-1">
        <BasicInputField
          id="referentEmail"
          type="email"
          description="Format attendu&nbsp;: nom@domaine.fr"
          bind:value={$orientation.referentEmail}
          vertical
        />
      </div>
    </div>
  </Fieldset>

  <Fieldset title="Le ou la bénéficiaire">
    <div class="flex flex-row justify-items-stretch gap-s24">
      <div class="flex-1">
        <BasicInputField
          id="beneficiaryLastName"
          placeholder=""
          bind:value={$orientation.beneficiaryLastName}
          vertical
        />
      </div>
      <div class="flex-1">
        <BasicInputField
          id="beneficiaryFirstName"
          placeholder=""
          bind:value={$orientation.beneficiaryFirstName}
          vertical
        />
      </div>
    </div>

    <BasicInputField
      id="beneficiaryAvailability"
      type="date"
      description=""
      bind:value={$orientation.beneficiaryAvailability}
      vertical
    >
      <p slot="description" class="legend italic">
        Date à partir de laquelle la personne est disponible.<br />
        Format attendu&nbsp;: JJ/MM/AAAA (par exemple, 17/01/2023 pour 17 janvier
        2023)
      </p>
    </BasicInputField>

    {#if $orientation.requirements.length || $orientation.situation.length}
      <div class="rounded-md bg-info-light px-s20 py-s20">
        <Accordion
          title="Profil et critères du ou de la bénéficiaire"
          subTitle="Récapitulatif des critères que vous avez confirmé à l’étape précédente."
          titleLevel="h3"
          noTitleMargin
          titleClass="text-f18"
          expanded={true}
        >
          <div class="mt-s20">
            {#if $orientation.situation.length}
              <h4 class="mb-s6 text-gray-text">
                Profil de votre bénéficiaire&nbsp;:
              </h4>
              <ul class="ml-s20 list-disc">
                {#each $orientation.situation as label}
                  {#if label === "Autre"}
                    <li class="text-gray-text">
                      {label}&nbsp;: {$orientation.situationOther}
                    </li>
                  {:else}
                    <li class="text-gray-text">{label}</li>
                  {/if}
                {/each}
              </ul>
            {/if}

            {#if $orientation.requirements.length}
              <h4 class="mb-s6 mt-s16 text-gray-text">
                Critères correspondants&nbsp;:
              </h4>
              <ul class="ml-s20 list-disc">
                {#each $orientation.requirements as label}
                  <li class="text-gray-text">{label}</li>
                {/each}
              </ul>
            {/if}
          </div>
        </Accordion>
      </div>
    {/if}

    <CheckboxesField
      id="beneficiaryContactPreferences"
      choices={contactPrefOptions}
      bind:value={$orientation.beneficiaryContactPreferences}
      vertical
      horizontalCheckboxes
    />

    <div class="flex flex-row justify-items-stretch gap-s24">
      <div class="flex-1">
        <BasicInputField
          id="beneficiaryPhone"
          type="tel"
          description="Format attendu&nbsp;: 0123456789"
          bind:value={$orientation.beneficiaryPhone}
          vertical
        />
      </div>
      <div class="flex-1">
        <BasicInputField
          id="beneficiaryEmail"
          type="email"
          description="Format attendu&nbsp;: nom@domaine.fr"
          bind:value={$orientation.beneficiaryEmail}
          vertical
        />
      </div>
    </div>

    {#if $orientation.beneficiaryContactPreferences.includes("AUTRE")}
      <TextareaField
        id="beneficiaryOtherContactMethod"
        description="Préciser quelle autre méthode de contact est possible"
        bind:value={$orientation.beneficiaryOtherContactMethod}
        vertical
      />
    {/if}

    <TextareaField
      id="orientationReasons"
      label={`Si besoin, détaillez ici le motif de l’orientation du bénéficiaire ${
        $orientation.beneficiaryFirstName || ""
      }
      ${$orientation.beneficiaryLastName || ""} pour le service "${
        service.name
      }"`}
      description="Merci de ne pas fournir des informations considérées comme sensibles (situation personnelle ou professionnelle autre que celles cochées à l’étape un de la demande, etc.)."
      bind:value={$orientation.orientationReasons}
      vertical
    />
  </Fieldset>

  {#if service.formsInfo.length || credentials.length}
    <Fieldset title="Documents et justificatifs requis">
      <Notice title="Mention d’information" titleLevel="h3" type="warning">
        <p class="m-s0 text-f14 text-gray-text">
          Attention à ne télécharger que les pièces strictement nécessaires à la
          demande.
          <strong>
            Pour des raisons de confidentialité, l’envoi de la carte vitale, des
            attestations de droits santé/CPAM ou de tout autre document
            contenant le NIR (numéro de sécurité sociale) n’est pas autorisé.
          </strong>
        </p>
      </Notice>

      {#each service.formsInfo as form}
        {#if $orientation.attachments[form.name]}
          <UploadField
            dynamicId
            label="Document à compléter"
            vertical
            id={form.name}
            description="Taille maximale&nbsp;: 5 Mo. Formats supportés&nbsp;: doc, docx, pdf, png, jpeg, jpg, odt, xls, xlsx, ods"
            bind:fileKeys={$orientation.attachments[form.name]}
          >
            <p slot="description">
              <a
                href={form.url}
                class="font-bold underline"
                target="_blank"
                rel="noopener nofollow ugc"
              >
                {formatFilePath(form.name)}
              </a>
            </p>
          </UploadField>
        {/if}
      {/each}

      {#each credentials as cred}
        {#if $orientation.attachments[cred.label]}
          <UploadField
            dynamicId
            label={cred.label}
            vertical
            id={cred.label}
            description="Taille maximale&nbsp;: 5 Mo. Formats supportés&nbsp;: doc, docx, pdf, png, jpeg, jpg, odt, xls, xlsx, ods"
            bind:fileKeys={$orientation.attachments[cred.label]}
          />
        {/if}
      {/each}
    </Fieldset>
  {/if}

  <div class="my-s32">
    <Notice
      type="info"
      title="L’accompagnateur s’engage à informer la personne concernée de ce traitement de données."
    />
  </div>
</div>
