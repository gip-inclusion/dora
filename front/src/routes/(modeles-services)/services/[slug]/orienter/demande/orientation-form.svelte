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
  import Alert from "$lib/components/display/alert.svelte";
  import Accordion from "$lib/components/display/accordion.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";
  import { orientationContainsTestWords } from "$lib/utils/orientation";
  import { userPreferences } from "$lib/utils/preferences";
  import type { Choice } from "$lib/types";
  import { URL_DOCUMENTATION_ORIENTATION } from "$lib/consts";
  import { formErrors } from "$lib/validation/validation";
  import type { Service } from "$lib/types";

  interface Props {
    service: Service;
    credentials: any;
  }

  let { service, credentials }: Props = $props();

  let contactPrefOptions: Choice[] = $state([]);

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
      { value: "REFERENT", label: "Via le conseiller référent" },
      { value: "AUTRE", label: "Autre" },
    ];

    $orientation.referentLastName = $userInfo.lastName;
    $orientation.referentFirstName = $userInfo.firstName;
    $orientation.referentEmail = $userInfo.email;
  });

  let testWordDetected = $derived(orientationContainsTestWords($orientation));
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

    <div class="gap-s24 flex flex-row justify-items-stretch">
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
    <div class="gap-s24 flex flex-row justify-items-stretch">
      <div class="flex-1">
        <BasicInputField
          id="referentPhone"
          type="tel"
          placeholder="0123456789"
          descriptionText="Format attendu&nbsp;: 4 à 10 caractères alphanumériques (sans l'indicatif pays)&nbsp;; ex. 0123456789"
          bind:value={$orientation.referentPhone}
          vertical
        />
      </div>
      <div class="flex-1">
        <BasicInputField
          id="referentEmail"
          type="email"
          placeholder="nom@domaine.fr"
          descriptionText="Saisissez votre adresse professionnelle. Format attendu&nbsp;: mail@domaine.fr"
          bind:value={$orientation.referentEmail}
          vertical
        />
      </div>
    </div>
  </Fieldset>

  <Fieldset title="Le ou la bénéficiaire">
    <BasicInputField
      id="beneficiaryFranceTravailNumber"
      placeholder=""
      descriptionText="Numéro unique à 11 chiffres"
      bind:value={$orientation.beneficiaryFranceTravailNumber}
      vertical
    />

    <div class="gap-s24 flex flex-row justify-items-stretch">
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
      descriptionText=""
      bind:value={$orientation.beneficiaryAvailability}
      vertical
    >
      {#snippet description()}
        <p class="legend italic">
          Date à partir de laquelle la personne est disponible.<br />
          Format attendu&nbsp;: JJ/MM/AAAA (par exemple, 17/01/2023 pour 17 janvier
          2023)
        </p>
      {/snippet}
    </BasicInputField>

    {#if $orientation.requirements.length || $orientation.situation.length}
      <div class="bg-info-light px-s20 py-s20 rounded-lg">
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

    <div class="gap-s24 flex flex-row justify-items-stretch">
      <div class="flex-1">
        <BasicInputField
          id="beneficiaryPhone"
          type="tel"
          placeholder="0123456789"
          descriptionText="Format attendu&nbsp;: 4 à 10 caractères alphanumériques (sans l'indicatif pays)&nbsp;; ex. 0123456789"
          bind:value={$orientation.beneficiaryPhone}
          vertical
        />
      </div>
      <div class="flex-1">
        <BasicInputField
          id="beneficiaryEmail"
          type="email"
          placeholder="nom@domaine.fr"
          descriptionText="Format attendu&nbsp;: nom@domaine.fr"
          bind:value={$orientation.beneficiaryEmail}
          vertical
        />
      </div>
    </div>

    {#if $orientation.beneficiaryContactPreferences.includes("AUTRE")}
      <TextareaField
        id="beneficiaryOtherContactMethod"
        descriptionText="Préciser quelle autre méthode de contact est possible"
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

  {#if service.formsInfo?.length || credentials.length}
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

      {#each service.formsInfo || [] as form}
        {#if $orientation.attachments[form.name]}
          <UploadField
            dynamicId
            label="Document à compléter"
            vertical
            id={form.name}
            descriptionText="Taille maximale&nbsp;: 5 Mo. Formats supportés&nbsp;: doc, docx, pdf, png, jpeg, jpg, odt, xls, xlsx, ods"
            bind:fileKeys={$orientation.attachments[form.name]}
          >
            {#snippet description()}
              <p>
                <a
                  href={form.url}
                  class="font-bold underline"
                  target="_blank"
                  rel="noopener nofollow ugc"
                >
                  {formatFilePath(form.name)}
                </a>
              </p>
            {/snippet}
          </UploadField>
        {/if}
      {/each}

      {#each credentials || [] as cred}
        {#if $orientation.attachments[cred.label]}
          <UploadField
            dynamicId
            label={cred.label}
            vertical
            id={cred.label}
            descriptionText="Taille maximale&nbsp;: 5 Mo. Formats supportés&nbsp;: doc, docx, pdf, png, jpeg, jpg, odt, xls, xlsx, ods"
            bind:fileKeys={$orientation.attachments[cred.label]}
          />
        {/if}
      {/each}

      {#if $formErrors?.beneficiaryAttachments}
        {#each $formErrors.beneficiaryAttachments as error, i}
          <Alert id="beneficiaryAttachments-{i}" label={error} />
        {/each}
      {/if}
    </Fieldset>
  {/if}

  <div class="my-s32 gap-s32 flex flex-col">
    {#if testWordDetected}
      <Notice
        type="error"
        title="Le mot «&#8239;{testWordDetected}&#8239;» a été détecté dans les champs…"
        ><p>
          Les orientations fictives/test nécessitent une vérification manuelle,
          augmentant la charge de travail de nos équipes. Pour découvrir le
          fonctionnement du formulaire, consultez plutôt <a
            href={URL_DOCUMENTATION_ORIENTATION}
            target="_blank"
            class="underline">notre documentation</a
          >.
        </p></Notice
      >
    {/if}
    <Notice
      type="info"
      title="L’accompagnateur s’engage à informer la personne concernée de ce traitement de données."
    />
  </div>
</div>
