<script>
  import { getApiURL } from "$lib/utils/api.js";
  import { deleteBinIcon } from "$lib/icons.js";

  export let structureSlug;
  export let fileKeys = [];
  export let disabled = false;
  export let name;

  let progress = null;
  let uploadInput;

  function handleRemove(fileKey) {
    fileKeys = fileKeys.filter((k) => k !== fileKey);
  }

  async function handleSubmit() {
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
      const url = `${getApiURL()}/upload/${structureSlug}/${file.name}/`;
      const request = new XMLHttpRequest();
      request.open("POST", url);
      request.setRequestHeader("Accept", "application/json; version=1.0");

      // upload progress event
      request.upload.addEventListener("progress", (e) => {
        // upload progress as percentage
        updateProgress(e.loaded, e.total);
      });

      // request finished event
      request.addEventListener("load", () => {
        handleUploadDone(request);
      });

      // send POST request to server
      request.send(file);
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="cursor-pointer mb-s8">
  <label>
    <input
      {name}
      bind:this={uploadInput}
      on:blur
      on:change={handleSubmit}
      {disabled}
      type="file"
      multiple
      class="file:px-s8 file:lg:px-s10 file:py-s6 file:text-f14 file:leading-normal file:border file:border-magenta-cta file:hover:border-magenta-hover file:disabled:border-gray-01 file:active:border-france-blue font-bold file:text-magenta-cta file:hover:text-white file:disabled:disabled:text-gray-text-alt2 file:active:text-france-blue file:bg-white file:hover:bg-magenta-hover file:rounded"
    />{progress != null ? `${Math.round(progress)} %` : ""}
  </label>
</form>
<ul>
  {#each fileKeys as uploaded}
    <li class="mb-s8 flex">
      <div class="text-f14">{uploaded}</div>
      <button
        on:click={handleRemove(uploaded)}
        class="w-s24 h-s24 ml-s16 fill-error"
      >
        {@html deleteBinIcon}
      </button>
    </li>
  {/each}
</ul>
