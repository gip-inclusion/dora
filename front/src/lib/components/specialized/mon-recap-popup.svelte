<script lang="ts">
	import dayjs from "dayjs";

  import { browser } from "$app/environment";
  import TallyPopup from "$lib/components/specialized/tally-popup.svelte";
  import { TallyFormId, MON_RECAP_DEPARTMENTS } from "$lib/consts";
  import { userInfo } from "$lib/utils/auth";

let monRecapTallyFormCompletedKey = `tallyForm-${TallyFormId.NOTEBOOK_ORDER_FORM_ID}-completed`;

let shouldDisplayMonRecapForm = 
  $userInfo &&
  ($userInfo.mainActivity === "accompagnateur" || $userInfo.mainActivity === "accompagnateur_offreur") &&
  $userInfo.structures.some(struct => MON_RECAP_DEPARTMENTS.includes(struct.department)) &&
  !localStorage.getItem(monRecapTallyFormCompletedKey);

</script>

{#if browser && shouldDisplayMonRecapForm}
  <TallyPopup
    formId={TallyFormId.NOTEBOOK_ORDER_FORM_ID}
    timeoutSeconds={3}
    minDaysBetweenDisplays={1}
    on:submit={() => {
      localStorage.setItem(monRecapTallyFormCompletedKey, dayjs().toString());
      shouldDisplayMonRecapForm = false;
    }}
  />
{/if}
