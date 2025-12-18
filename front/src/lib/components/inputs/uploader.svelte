<script lang="ts">
  import DeleteBinLineSystem from "svelte-remix/DeleteBinLineSystem.svelte";

  import { getApiURL } from "$lib/utils/api";
  import { getToken } from "$lib/utils/auth";
  import { shortenString } from "$lib/utils/misc";

  import Alert from "../display/alert.svelte";

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

  function handleRemove(fileKey: string) {
    fileKeys = fileKeys.filter((key) => key !== fileKey);
  }

  function clearInput() {
    uploadInput.value = "";
    uploadInput.disabled = false;
    progress = null;
  }

  function handleSubmit(event: Event) {
    event.preventDefault();

    function updateProgress(loaded: number, total: number) {
      progress = (loaded / total) * 100;
    }

    function handleUploadDone(request: XMLHttpRequest) {
      const jsonResponse = JSON.parse(request.response);
      fileKeys = [jsonResponse.key, ...fileKeys];
      clearInput();
      errorMessage = "";
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

      // We can't use fetch if we want a progress indicator
      const url = structureSlug
        ? `${getApiURL()}/upload/${structureSlug}/${file.name}/`
        : `${getApiURL()}/safe-upload/${file.name}/`;
      const request = new XMLHttpRequest();
      request.open("POST", url);
      request.setRequestHeader("Accept", "application/json; version=1.0");
      request.setRequestHeader("Authorization", `Token ${getToken()}`);

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
              errorMessage = `Erreur lors de l'envoi du fichier "${file.name}"`;
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
  }

  function urlStringPathRemove(path: string): string {
    const pathElements = path.split("/");
    return pathElements[pathElements.length - 1] ?? "";
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
  {#each fileKeys as uploaded}
    <li class="mb-s8 flex justify-between">
      <div class="text-f14">{shortenString(urlStringPathRemove(uploaded))}</div>
      <div class="h-s24 w-s24">
        <button
          onclick={() => handleRemove(uploaded)}
          class="ml-s16 h-s24 w-s24 fill-error"
        >
          <DeleteBinLineSystem />
        </button>
      </div>
    </li>
  {/each}
</ul>
