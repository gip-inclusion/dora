<script lang="ts">
  import { onMount } from "svelte";
  import { toast } from "@zerodevx/svelte-toast";

  import illuAccompagner from "$lib/assets/illustrations/illu-accompagner.svg";
  import Button from "$lib/components/display/button.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import {
    getOrientationExport,
    requestOrientationExportLink,
    type OrientationExportType,
  } from "$lib/requests/orientations";
  import { userInfo } from "$lib/utils/auth";
  import { ORIENTATIONS_EXPORT_LINK_VALIDITY_MINUTES } from "$lib/consts";

  import { generateOrientationExport } from "../suivi/orientation-export";

  interface Props {
    structureSlug: string;
    type: OrientationExportType;
    token: string;
  }
  const { structureSlug, type, token }: Props = $props();

  type Status = "loading" | "downloaded" | "empty" | "expired" | "error";

  let status = $state<Status>("loading");
  let isSendingLink = $state(false);
  let linkSent = $state(false);

  const typeLabel = $derived(type === "sent" ? "envoyées" : "reçues");

  onMount(async () => {
    const result = await getOrientationExport(structureSlug, token);

    if (result.status === 410) {
      status = "expired";
    } else if (!result.data) {
      status = "error";
    } else if (result.data.length === 0) {
      status = "empty";
    } else {
      await generateOrientationExport(structureSlug, type, result.data);
      status = "downloaded";
    }
  });

  async function sendNewLink() {
    isSendingLink = true;
    const result = await requestOrientationExportLink(structureSlug, type);
    isSendingLink = false;

    if (result.ok) {
      linkSent = true;
    } else {
      toast.push(
        "Une erreur est survenue lors de l’envoi du lien de téléchargement."
      );
    }
  }
</script>

<div class="my-s24">
  {#if status === "loading"}
    <p>Préparation du fichier des orientations {typeLabel}…</p>
  {:else if status === "downloaded"}
    <Notice type="success" title="Téléchargement lancé">
      <p class="text-f14 mb-s0">
        Le fichier des orientations {typeLabel} a été téléchargé.
      </p>
    </Notice>
  {:else if status === "empty"}
    <Notice type="info" title="Aucune orientation à télécharger" />
  {:else if status === "error"}
    <Notice type="error" title="Lien de téléchargement invalide">
      <p class="text-f14 mb-s0">
        Ce lien ne peut être utilisé que par la personne qui l’a demandé. Vous
        pouvez demander un nouveau lien depuis la page de suivi des
        orientations.
      </p>
    </Notice>
  {:else if linkSent}
    <Notice type="success" title="Envoi validé">
      <p class="text-f14 mb-s0">
        Le lien de téléchargement sécurisé a été envoyé à votre adresse mail
        {$userInfo?.email}. Il est valable
        {ORIENTATIONS_EXPORT_LINK_VALIDITY_MINUTES} minutes.
      </p>
    </Notice>
  {:else}
    <div
      class="px-s20 py-s32 gap-s32 border-gray-03 flex flex-row justify-center border-2 border-dashed text-center"
    >
      <div class="gap-s12 flex flex-2 flex-col items-center justify-center">
        <h2 class="text-gray-text">Lien expiré</h2>
        <p>
          Le lien de téléchargement a une durée de validité de
          {ORIENTATIONS_EXPORT_LINK_VALIDITY_MINUTES} minutes
        </p>
        <Button
          label="Recevoir un nouveau lien"
          onclick={sendNewLink}
          disabled={isSendingLink}
        />
      </div>
      <div class="hidden flex-1 md:flex">
        <img src={illuAccompagner} alt="" class="w-full" />
      </div>
    </div>
  {/if}

  {#if status !== "loading"}
    <p class="mt-s24">
      <a class="text-magenta-cta font-bold" href="/orientations/suivi"
        >Retour au suivi des orientations</a
      >
    </p>
  {/if}
</div>
