<script lang="ts">
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  import LinkButton from "$lib/components/display/link-button.svelte";

  interface Props {
    url: string;
  }

  let { url }: Props = $props();

  function addTrackingParamsToUrl(urlStr: string) {
    const urlObj = new URL(urlStr);
    urlObj.searchParams.append("at_medium", "custom1");
    urlObj.searchParams.append("at_campaign", "MA");
    urlObj.searchParams.append("at_custom1", "Dora");
    urlObj.searchParams.append("at_custom2", "Mob");
    urlObj.searchParams.append("at_custom3", "France0924");
    return urlObj.toString();
  }

  let urlWithTrackingParams = $derived(addTrackingParamsToUrl(url));
</script>

<div class="border-gray-02 p-s32 rounded-2xl border shadow-sm">
  <h2 class="text-f23 text-france-blue">Vous êtes un particulier ?</h2>
  <LinkButton
    id="mtm-bloc-mes-aides-page-service"
    to={urlWithTrackingParams}
    label="Faire une demande"
    icon={ExternalLinkLineSystem}
    iconOnRight
    otherTab
    wFull
  />
</div>
