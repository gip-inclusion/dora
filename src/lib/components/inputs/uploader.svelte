<script lang="ts">
  import { deleteBinIcon } from "$lib/icons";
  import { getApiURL } from "$lib/utils/api";
  import { shortenString } from "$lib/utils/misc";

  export let id: string;
  export let structureSlug: string | undefined;
  export let fileKeys: string[] = [];
  export let disabled = false;

  let progress: number | null = null;
  let uploadInput: HTMLInputElement;

  function handleRemove(fileKey) {
    fileKeys = fileKeys.filter((key) => key !== fileKey);
  }

  function handleSubmit() {
    function updateProgress(loaded, total) {
      progress = (loaded / total) * 100;
    }

    function handleUploadDone(request) {
      const jsonResponse = JSON.parse(request.response);
      fileKeys = [jsonResponse.key, ...fileKeys];
      // Clear input
      uploadInput.value = null;
      uploadInput.disabled = false;
      progress = null;
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

      // request finished event
      request.addEventListener("load", () => {
        handleUploadDone(request);
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
      accept=".doc, .docx, .pdf, .png, .jpeg, .jpg, .odt"
      multiple
      class="font-bold file:rounded file:border file:border-magenta-cta file:bg-white file:px-s8 file:py-s6 file:text-f14 file:leading-normal file:text-magenta-cta file:hover:border-magenta-hover file:hover:bg-magenta-hover file:hover:!text-white file:active:border-france-blue file:active:text-france-blue file:disabled:border-gray-01 file:disabled:disabled:text-gray-text-alt2 file:lg:px-s10"
    />{progress != null ? `${Math.round(progress)} %` : ""}
  </label>
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
