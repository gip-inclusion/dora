<script lang="ts">
  import dayjs from "dayjs";

  import { browser } from "$app/environment";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import { TallyFormId, MON_RECAP_DEPARTMENTS } from "$lib/consts";
  import { userInfo } from "$lib/utils/auth";
  import { userPreferences } from "$lib/utils/preferences";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";

  const monRecapTallyFormCompletedKey = `tallyForm-${TallyFormId.NOTEBOOK_ORDER_FORM_ID}-completed`;

  $: lastVisitedStructure = getCurrentlySelectedStructure(
    $userInfo,
    $userPreferences
  );

  $: shouldDisplayMonRecapForm =
    $userInfo &&
    ($userInfo.mainActivity === "accompagnateur" ||
      $userInfo.mainActivity === "accompagnateur_offreur") &&
    lastVisitedStructure &&
    lastVisitedStructure.canEditInformations &&
    MON_RECAP_DEPARTMENTS.includes(lastVisitedStructure.department) &&
    !localStorage.getItem(monRecapTallyFormCompletedKey);

  const hiddenFields = { source: "dora" };
</script>

{#if browser && shouldDisplayMonRecapForm}
  <TallyPopup
    formId={TallyFormId.NOTEBOOK_ORDER_FORM_ID}
    timeoutSeconds={12}
    minDaysBetweenDisplays={1}
    {hiddenFields}
    on:submit={() => {
      localStorage.setItem(monRecapTallyFormCompletedKey, dayjs().toString());
      shouldDisplayMonRecapForm = false;
    }}
  />
{/if}
