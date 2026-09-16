<script lang="ts">
  import DeleteBinLineSystem from "svelte-remix/DeleteBinLineSystem.svelte";

  import { getApiURL } from "$lib/utils/api";
  import { getFileNameFromPath, toValidFileName } from "$lib/utils/file";
  import { shortenString } from "$lib/utils/misc";

  import Alert from "../display/alert.svelte";
  import { deleteFile } from "$lib/requests/upload";

  interface Props {
    id: string;
    structureSlug?: string;
    fileKeys?: string[];
    disabled?: boolean;
    onblur?: (event: Event) => void;
  }

  let {
    id,
    structureSlug,
    fileKeys = $bindable([]),
    disabled = false,
    onblur,
  }: Props = $props();

  let uploadInput: HTMLInputElement;

  let errorMessage = $state("");
  let progress: number | null = $state(null);

  let localFiles = $state<string[]>([]);

  // Une clé de stockage identifie un document : deux fois la même clé désigne le même
  // fichier, pas deux pièces jointes. Les doublons hérités (services issus d’un modèle,
  // données antérieures au contrôle d’unicité) sont écartés à la lecture, et la liste
  // repart dédoublonnée à la première modification.
  $effect(() => {
    localFiles = [...new Set(fileKeys)];
  });

  function updateFiles(newFiles: string[]) {
    const uniqueFiles = [...new Set(newFiles)];
    localFiles = uniqueFiles;
    fileKeys = uniqueFiles;
  }

  async function handleRemove(fileKey: string) {
    const isFileDeleted = await deleteFile(fileKey);

    if (isFileDeleted) {
      updateFiles(localFiles.filter((key) => key !== fileKey));
    }
  }

  function clearInput() {
    uploadInput.value = "";
    uploadInput.disabled = false;
    progress = null;
  }

  function handleSubmit(event: Event) {
    event.preventDefault();

    // Deux documents de même nom se recouvrent : le serveur range les fichiers d’une
    // structure sous une clé dérivée de leur nom, et le second écraserait le premier.
    // On les écarte avant l’envoi, en tenant compte des fichiers du même lot, et en
    // comparant les noms nettoyés comme le fera le serveur.
    const usedFileNames = new Set(
      localFiles.map((key) => toValidFileName(getFileNameFromPath(key)))
    );
    const duplicateFileNames: string[] = [];

    function updateProgress(loaded: number, total: number) {
      progress = (loaded / total) * 100;
    }

    function handleUploadDone(request: XMLHttpRequest) {
      const jsonResponse = JSON.parse(request.response);
      updateFiles([jsonResponse.key, ...localFiles]);
      clearInput();
      if (!duplicateFileNames.length) {
        errorMessage = "";
      }
    }

    uploadInput.disabled = true;

    const files = uploadInput.files;

    if (!files) {
      return;
    }

    for (let i = 0; i < files.length; i++) {
      const file = files.item(i);
      if (!file) {
        continue;
      }

      const uploadedFileName = toValidFileName(file.name);
      if (usedFileNames.has(uploadedFileName)) {
        duplicateFileNames.push(file.name);
        continue;
      }
      usedFileNames.add(uploadedFileName);

      // We can't use fetch if we want a progress indicator
      const url = structureSlug
        ? `${getApiURL()}/upload/${structureSlug}/${file.name}/`
        : `${getApiURL()}/safe-upload/${file.name}/`;
      const request = new XMLHttpRequest();
      request.open("POST", url);
      request.setRequestHeader("Accept", "application/json; version=1.0");

      // upload progress event
      request.upload.addEventListener("progress", (progressEvent) => {
        // upload progress as percentage
        updateProgress(progressEvent.loaded, progressEvent.total);
      });

      // upload progress event
      request.upload.addEventListener("error", () => {
        errorMessage = `Erreur lors de l’envoi du fichier ${file.name}`;
        clearInput();
      });

      request.upload.addEventListener("abort", () => {
        errorMessage = `Erreur lors de l’envoi du fichier ${file.name}`;
        clearInput();
      });

      request.upload.addEventListener("timeout", () => {
        errorMessage = `Erreur lors de l’envoi du fichier ${file.name}`;
        clearInput();
      });

      // request finished event
      request.addEventListener("load", (progressEvent: ProgressEvent) => {
        const target = progressEvent.target as XMLHttpRequest;
        if (target.status !== 201) {
          let message = "";
          clearInput();
          try {
            message = JSON.parse(target.response)[0].message;

            if (message === "INVALID_EXTENSION") {
              errorMessage = `Le fichier "${file.name}" n’est pas au bon format`;
            } else if (message === "FILE_TOO_BIG") {
              errorMessage = `Le fichier "${file.name}" est trop volumineux`;
            } else if (message === "INVALID_FILE_CONTENT") {
              errorMessage = `Le contenu du fichier "${file.name}" ne correspond pas à son extension`;
            } else if (message === "FILENAME_TOO_LONG") {
              errorMessage = `Le nom du fichier "${file.name}" est trop long`;
            } else if (message === "MISSING_EXTENSION") {
              errorMessage = `Le fichier "${file.name}" doit avoir une extension`;
            } else {
              errorMessage = `Erreur lors du traitement du fichier "${file.name}"`;
            }
          } catch {
            errorMessage = `Erreur lors de l’envoi du fichier "${file.name}"`;
          }
        } else {
          handleUploadDone(request);
        }
      });

      // send POST request to server
      const formData = new FormData();
      formData.append("file", file);
      request.send(formData);
    }

    if (duplicateFileNames.length) {
      errorMessage =
        duplicateFileNames.length > 1
          ? `Des documents portant les noms ${duplicateFileNames.map((name) => `“${name}”`).join(", ")} sont déjà présents. Renommez-les avant de les ajouter.`
          : `Un document nommé “${duplicateFileNames[0]}” est déjà présent. Renommez-le avant de l’ajouter.`;
    }

    if (duplicateFileNames.length === files.length) {
      clearInput();
    }
  }
</script>

<form onsubmit={handleSubmit} class="mb-s8 cursor-pointer">
  <label>
    <input
      name={id}
      {id}
      bind:this={uploadInput}
      {onblur}
      onchange={handleSubmit}
      {disabled}
      type="file"
      accept=".doc, .docx, .pdf, .png, .jpeg, .jpg, .odt, .xls, .xlsx, .ods"
      multiple
      class="file:border-magenta-cta file:px-s8 file:py-s6 file:text-f14 file:text-magenta-cta read-only:text-gray-text file:hover:border-magenta-hover file:hover:bg-magenta-hover file:active:border-france-blue file:active:text-france-blue file:disabled:border-gray-01 file:disabled:text-gray-text-alt2 lg:file:px-s10 file:rounded-sm file:border file:bg-white file:leading-normal file:hover:text-white!"
    />{progress != null ? `${Math.round(progress)} %` : ""}
  </label>

  {#if errorMessage}
    <Alert id="{id}-error" label={errorMessage} />
  {/if}
</form>
<ul>
  {#each localFiles as uploaded (uploaded)}
    <li class="mb-s8 flex justify-between">
      <div class="text-f14">{shortenString(getFileNameFromPath(uploaded))}</div>
      <div class="h-s24 w-s24">
        <button
          type="button"
          onclick={() => handleRemove(uploaded)}
          class="ml-s16 h-s24 w-s24 fill-error"
        >
          <DeleteBinLineSystem />
        </button>
      </div>
    </li>
  {/each}
</ul>
