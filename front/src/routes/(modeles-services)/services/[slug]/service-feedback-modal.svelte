<script lang="ts">
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";

  import illustration from "$lib/assets/illustrations/Validation_Orientation_Envoyee.webp";

  import Button from "$lib/components/display/button.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  import type { Service } from "$lib/types";
  import { customFetch, getApiURL } from "$lib/utils/api";
  import { userInfo } from "$lib/utils/auth";
  import * as v from "$lib/validation/schema-utils";
  import { validate } from "$lib/validation/validation";

  interface Props {
    isOpen?: boolean;
    service: Service;
  }

  let { isOpen = $bindable(false), service }: Props = $props();

  const isDI = "source" in service;

  const allReasons = [
    {
      label:
        "Les aspects administratifs sont incorrects ou incomplets (critères d'éligibilité, public concerné, documents requis)",
    },
    {
      label:
        "Les informations pratiques sont obsolètes (modalités d'accueil, horaires, contacts, adresse)",
    },
    {
      label:
        "La zone d'intervention est inexacte (territoire couvert, périmètre d'action)",
    },
    {
      label:
        "Le service ne correspond pas aux critères DORA (nature du service, missions d'insertion)",
      notifySupport: true,
    },
    {
      label:
        "Les partenariats ou dispositifs mentionnés n'existent plus ou sont temporairement suspendus (services suspendus, conventions terminées)",
      notifySupport: true,
    },
    { label: "Le délai de traitement/d'attente indiqué n'est plus valable" },
    { label: "Autre motif (merci de préciser)", other: true },
  ];
  const reasonOptions = allReasons.map(({ label }) => ({
    label,
    value: label,
  }));
  const notifySupportReasonLabels = allReasons
    .filter(({ notifySupport }) => notifySupport)
    .map(({ label }) => label);
  const otherReasonLabel = allReasons.find(({ other }) => other)?.label;

  let isRequesting = $state(false);
  let isFeedbackSent = $state(false);
  let formPage: 1 | 2 = $state(1);
  let selectedReasons: string[] = $state([]);
  let otherReason = $state("");
  let name = $state("");
  let email = $state("");
  let details = $state("");

  function resetState() {
    isRequesting = false;
    isFeedbackSent = false;
    formPage = 1;
    selectedReasons = [];
    otherReason = "";
    name = $userInfo ? `${$userInfo.firstName} ${$userInfo.lastName}` : "";
    email = $userInfo ? $userInfo.email : "";
    details = "";
  }

  $effect(() => {
    if (!isOpen) {
      // Réinitialisation automatique lorsque la modale est fermée
      resetState();
    }
  });

  let formData = $derived({
    selectedReasons,
    otherReason,
    name,
    email,
    details,
  });

  function isOtherReasonSelected(reasons: string[]) {
    return Boolean(otherReasonLabel && reasons.includes(otherReasonLabel));
  }

  function isNotifySupportReasonSelected(reasons: string[]) {
    return notifySupportReasonLabels.some((reason) => reasons.includes(reason));
  }

  const feedbackSchemaPage1: v.Schema = {
    selectedReasons: {
      label: "Sélectionner une raison",
      default: "",
      rules: [v.isArray([v.isString()])],
      required: true,
    },
    otherReason: {
      label: "Autre motif (merci de préciser)",
      default: "",
      rules: [v.isString()],
      required: (data) => isOtherReasonSelected(data.selectedReasons),
    },
  };

  const feedbackSchemaPage2: v.Schema = {
    name: {
      label: "Votre nom",
      default: "",
      rules: [v.isString(), v.maxStrLength(140)],
      post: [v.trim],
      required: true,
    },
    email: {
      label: "Courriel",
      default: "",
      rules: [v.isEmail(), v.maxStrLength(254)],
      post: [v.lower, v.trim],
      required: true,
    },
    details: {
      label: "Précisez votre signalement",
      default: "",
      rules: [v.isString()],
      required: true,
    },
  };

  const feedbackSchema = {
    ...feedbackSchemaPage1,
    ...feedbackSchemaPage2,
  };

  onMount(() => {
    if ($userInfo) {
      name = `${$userInfo.firstName} ${$userInfo.lastName}`;
      email = $userInfo.email;
    }
  });

  function handleClose() {
    resetState();
    isOpen = false;
  }

  function handleContinue() {
    const { valid } = validate(formData, feedbackSchemaPage1);
    if (valid) {
      formPage = 2;
    }
  }

  function handleSubmit() {
    const url = `${getApiURL()}/services${isDI ? "-di" : ""}/${
      service.slug
    }/feedback/`;

    return customFetch(url, {
      method: "POST",
      body: JSON.stringify({
        reasons: [
          ...selectedReasons.filter((reason) => reason !== otherReasonLabel),
          ...(isOtherReasonSelected(selectedReasons) ? [otherReason] : []),
        ],
        notifySupport: isNotifySupportReasonSelected(selectedReasons),
        name,
        email,
        details,
      }),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
  }

  function handleSuccess(_jsonResult) {
    isFeedbackSent = true;
  }
</script>

<Modal width="small" bind:isOpen title="Vous avez une suggestion ?">
  {#if !isFeedbackSent}
    <div in:slide={{ duration: 300 }} out:slide={{ duration: 300 }}>
      <Form
        bind:data={formData}
        schema={feedbackSchema}
        onSubmit={handleSubmit}
        onSuccess={handleSuccess}
        bind:requesting={isRequesting}
      >
        <fieldset class="gap-s16 flex flex-col">
          {#if formPage === 1}
            <div in:slide={{ duration: 300 }} out:slide={{ duration: 300 }}>
              <div class="text-f16 leading-s24 text-gray-text">
                Aidez-nous à améliorer la qualité de nos contenus en signalant
                une erreur, une information manquante ou inexacte.
              </div>
              <CheckboxesField
                id="selectedReasons"
                bind:value={selectedReasons}
                choices={reasonOptions}
                vertical
              />
              {#if isOtherReasonSelected(selectedReasons)}
                <BasicInputField
                  id="otherReason"
                  bind:value={otherReason}
                  vertical
                  hideLabel
                />
              {/if}
            </div>
          {:else if formPage === 2}
            <div in:slide={{ duration: 300 }} out:slide={{ duration: 300 }}>
              <BasicInputField id="name" bind:value={name} vertical />
              <BasicInputField id="email" bind:value={email} vertical />
              <TextareaField
                id="details"
                bind:value={details}
                vertical
                description="Décrivez les modifications nécessaires pour nous permettre de mettre à jour cette fiche. Plus votre description sera détaillée, plus nous pourrons traiter efficacement votre signalement."
              />
              <div class="text-f16 leading-s24 text-gray-text">
                En soumettant ce formulaire, vous acceptez que vos données
                soient utilisées pour le traitement de votre signalement, et
                uniquement à cet effet.
              </div>
            </div>
          {/if}
          <div class="mt-s12 gap-s16 flex justify-end">
            <Button label="Annuler" secondary onclick={handleClose} />
            {#if formPage === 1}
              <Button label="Continuer" onclick={handleContinue} />
            {:else if formPage === 2}
              <Button label="Envoyer" type="submit" disabled={isRequesting} />
            {/if}
          </div>
        </fieldset>
      </Form>
    </div>
  {:else}
    <div in:slide={{ duration: 300 }} out:slide={{ duration: 300 }}>
      <div class="text-center">
        <img
          class="mx-auto w-[320px]"
          src={illustration}
          alt=""
          aria-hidden="true"
        />
        <h2 class="text-f17 text-gray-text leading-s24 mb-s4 font-bold">
          Merci pour votre signalement !
        </h2>
        <span class="text-f14 text-gray-text leading-s24">
          La structure concernée sera informée des modifications suggérées.
        </span>
      </div>
    </div>
  {/if}
</Modal>
