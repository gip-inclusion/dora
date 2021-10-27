<script>
  import { getApiURL } from "$lib/utils/api.js";

  export let structureSlug;
  export let fileKeys = [];
  export let disabled = false;
  export let name;

  let progress = null;
  let uploadInput;

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

<form on:submit|preventDefault={handleSubmit}>
  <label>
    <input
      {name}
      bind:this={uploadInput}
      on:blur
      on:change={handleSubmit}
      {disabled}
      type="file"
      multiple
    />{progress != null ? `${Math.round(progress)} %` : ""}</label
  >
</form>
<ul>
  {#each fileKeys as uploaded}
    <li>• {uploaded}</li>
  {/each}
</ul>
