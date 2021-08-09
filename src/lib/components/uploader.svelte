<script>
  import { getApiURL } from "$lib/utils";
  export let fileKeys = [];
  export let disabled;
  let progress = null;
  let uploadInput;

  async function handleSubmit() {
    uploadInput.disabled = true;

    let files = uploadInput.files;
    for (let i = 0; i < files.length; i++) {
      const file = files.item(i);
      // We can't use fetch if we want a progress indicator
      const url = `${getApiURL()}/upload/${file.name}/`;
      const request = new XMLHttpRequest();
      request.open("POST", url);
      request.setRequestHeader("Accept", "application/json; version=1.0");

      // upload progress event
      request.upload.addEventListener("progress", function (e) {
        // upload progress as percentage
        progress = (e.loaded / e.total) * 100;
      });

      // request finished event
      request.addEventListener("load", function () {
        // HTTP status message (200, 404 etc)
        console.log("done", request.status);
        // request.response holds response from the server
        console.log(request.response);
        const jsonResponse = JSON.parse(request.response);
        fileKeys = [jsonResponse.key, ...fileKeys];
        // Clear input
        uploadInput.value = null;
        uploadInput.disabled = false;
        progress = null;
      });

      // send POST request to server
      request.send(file);
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <label>
    Ajouter un fichier
    <input
      bind:this={uploadInput}
      on:change={handleSubmit}
      {disabled}
      type="file"
      multiple />{progress != null ? Math.round(progress) + " %" : ""}</label>
</form>
<ul>
  {#each fileKeys as uploaded}
    <li>• {uploaded}</li>
  {/each}
</ul>
