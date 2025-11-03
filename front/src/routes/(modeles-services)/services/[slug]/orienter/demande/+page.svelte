<script lang="ts">
  import { get } from "svelte/store";

  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import StickyFormSubmissionRow from "$lib/components/forms/sticky-form-submission-row.svelte";
  import { getApiURL } from "$lib/utils/api";
  import { token } from "$lib/utils/auth";
  import Layout from "../orientation-layout.svelte";
  import type { PageData } from "./$types";
  import { orientation } from "../store";
  import OrientationForm from "./orientation-form.svelte";
  import ContactBox from "../contact-box.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import { orientationStep2Schema } from "../schema";
  import Form from "$lib/components/forms/form.svelte";
  import { goto } from "$app/navigation";
  import ArrowLeftSLineArrows from "svelte-remix/ArrowLeftSLineArrows.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  const { service } = data;
  const isDI = !!data.isDI;

  let requesting = $state(false);

  // Fichiers à uploader
  const credentials = (service.credentialsDisplay || [])
    .filter(
      (elt) => !elt.toLowerCase().includes("vitale") && elt.label !== "Aucun"
    )
    .map((value) => ({ value: value, label: value }));

  credentials.forEach((cred) => {
    $orientation.attachments[cred.label] = [];
  });
  (service.formsInfo || []).forEach((form) => {
    $orientation.attachments[form.name] = [];
  });

  function handleChange(validatedData) {
    $orientation = { ...validatedData };
  }

  function handleSubmit(validatedData) {
    const beneficiaryAttachments = Object.values(
      validatedData.attachments
    ).flat();

    return fetch(`${getApiURL()}/orientations/`, {
      method: "POST",
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",
        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify({
        ...validatedData,
        serviceSlug: isDI ? null : service.slug,
        diServiceId: isDI ? service.slug : "",
        diServiceName: isDI ? service.name || "" : "",
        diServiceAddressLine: isDI ? service.addressLine : "",
        diContactEmail: isDI ? service.contactEmail || "" : "",
        diContactName: isDI ? service.contactName || "" : "",
        diContactPhone: isDI ? service.contactPhone || "" : "",
        diStructureName: isDI ? service.structureInfo.name || "" : "",
        beneficiaryAttachments,
      }),
    });
  }

  function handleSuccess(resultOrientation) {
    goto(
      `/services/${isDI ? "di--" : ""}${service.slug}/orienter/${resultOrientation.status === "MODÉRATION_EN_COURS" ? "moderation" : "merci"}`
    );
  }
</script>

<EnsureLoggedIn>
  <FormErrors />

  <Form
    bind:data={$orientation}
    schema={orientationStep2Schema}
    disableExitWarning
    onChange={handleChange}
    onSubmit={handleSubmit}
    onSuccess={handleSuccess}
    bind:requesting
  >
    <Layout {data}>
      <p class="legend">Étape 2 sur 2</p>

      <h2>Compléter la demande</h2>
      <hr class="my-s40" />
      <p class="mb-s40 text-f18 max-w-2xl">
        Ce formulaire collecte les informations nécessaires pour la demande
        d’orientation. Veuillez fournir tous les éléments demandés.
      </p>
      <p>
        Vous recevrez une copie de cette demande, tout comme le ou la
        bénéficiaire.
      </p>

      <div class="gap-x-s24 flex flex-col justify-between md:flex-row">
        <OrientationForm {credentials} {service} />
        <div class="mb-s32 w-full shrink-0 md:w-[384px]">
          <ContactBox {service} {isDI} />
        </div>
      </div>
    </Layout>

    <StickyFormSubmissionRow justifyBetween>
      <LinkButton
        icon={ArrowLeftSLineArrows}
        to="/services/{data.service.slug}/orienter"
        label="Revenir à l’étape précédente"
        secondary
      />

      <Button
        id="publish"
        type="submit"
        disabled={requesting}
        label="Envoyer l’orientation"
      />
    </StickyFormSubmissionRow>
  </Form>
</EnsureLoggedIn>
