<script lang="ts">
  import { deleteBinIcon } from "$lib/icons";
  import { getApiURL } from "$lib/utils/api";
  import { shortenString } from "$lib/utils/misc";
  import Alert from "../display/alert.svelte";

  export let id: string;
  export let structureSlug: string | undefined;
  export let fileKeys: string[] = [];
  export let disabled = false;

  let errorMessage = "";
  let progress: number | null = null;
  let uploadInput: HTMLInputElement;

  function handleRemove(fileKey) {
    fileKeys = fileKeys.filter((key) => key !== fileKey);
  }

  function clearInput() {
    uploadInput.value = null;
    uploadInput.disabled = false;
    progress = null;
  }

  function handleSubmit() {
    function updateProgress(loaded, total) {
      progress = (loaded / total) * 100;
    }

    function handleUploadDone(request) {
      const jsonResponse = JSON.parse(request.response);
      fileKeys = [jsonResponse.key, ...fileKeys];
      clearInput();
      errorMessage = "";
    }

    uploadInput.disabled = true;

    const files = uploadInput.files;

    for (let i = 0; i < files.length; i++) {
      const file = files.item(i);
      // We can't use fetch if we want a progress indicator
      const url = structureSlug
        ? `${getApiURL()}/upload/${structureSlug}/${file.name}/`
        : `${getApiURL()}/safe-upload/${file.name}/`;
      const request = new XMLHttpRequest();
      request.open("POST", url);
      request.setRequestHeader("Accept", "application/json; version=1.0");

      // upload progress event
      request.upload.addEventListener("progress", (event) => {
        // upload progress as percentage
        updateProgress(event.loaded, event.total);
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
      request.addEventListener("load", (event) => {
        if (event.target.status !== 201) {
          let message = "";
          clearInput();
          try {
            message = JSON.parse(event.target.response)[0].message;

            if (message === "INVALID_EXTENSION") {
              errorMessage = `Le fichier "${file.name}" n’est pas au bon format`;
            } else if (message === "FILE_TOO_BIG") {
              errorMessage = `Le fichier "${file.name}" est trop volumineux`;
            } else {
              errorMessage = `Erreur lors de l’envoi du fichier "${file.name}"`;
            }
          } catch {
            errorMessage = `Erreur lors de l’envoi du fichier "${file.name}"`;
          }
        } else {
          handleUploadDone(request);
        }
      });

      // send POST request to server
      request.send(file);
    }
  }

  function urlStringPathRemove(string) {
    const pathElements = string.split("/");
    return pathElements[pathElements.length - 1];
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="mb-s8 cursor-pointer">
  <label>
    <input
      name={id}
      {id}
      bind:this={uploadInput}
      on:blur
      on:change={handleSubmit}
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
          on:click={handleRemove(uploaded)}
          class="ml-s16 h-s24 w-s24 fill-error"
        >
          {@html deleteBinIcon}
        </button>
      </div>
    </li>
  {/each}
</ul>
