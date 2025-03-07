<script lang="ts">
  import dayjs from "dayjs";

  import { browser } from "$app/environment";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import { TallyFormId, MON_RECAP_DEPARTMENTS } from "$lib/consts";
  import { userInfo } from "$lib/utils/auth";

  const monRecapTallyFormCompletedKey = `tallyForm-${TallyFormId.NOTEBOOK_ORDER_FORM_ID}-completed`;

  let shouldDisplayMonRecapForm =
    $userInfo &&
    ($userInfo.mainActivity === "accompagnateur" ||
      $userInfo.mainActivity === "accompagnateur_offreur") &&
    $userInfo.structures.some((struct) =>
      MON_RECAP_DEPARTMENTS.includes(struct.department)
    ) &&
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
