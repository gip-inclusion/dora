<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { externalLinkIcon } from "$lib/icons";

  export let url: string;
</script>

<div class="rounded-ml border border-gray-02 p-s32 shadow-sm">
  <h2 class="text-f23 text-france-blue">Vous êtes un particulier ?</h2>
  <LinkButton
    id="mtm-bloc-mes-aides-page-service"
    to={url}
    label="Faire une demande"
    icon={externalLinkIcon}
    iconOnRight
    otherTab
    wFull
  />
</div>
