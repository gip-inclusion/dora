<script lang="ts">
  import UpdateStatusIcon from "$lib/components/specialized/services/update-status-icon.svelte";
  import DateLabel from "$lib/components/display/date-label.svelte";
  import type { Service } from "$lib/types";
  import dayjs from "dayjs";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";

  export let service: Service;

  const monthDiff = dayjs().diff(service.modificationDate, "month");
</script>

<div
  class="flex w-full flex-col place-content-between items-center gap-s24 text-gray-text md:flex-row"
>
  <div id="label-container">
    {#if service.status === "PUBLISHED"}
      {#if service.updateStatus === "NOT_NEEDED"}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon updateStatus={service.updateStatus} />
          </span>

          <RelativeDateLabel
            date={service.modificationDate}
            prefix="Actualisé"
          />
        </div>
      {:else if service.updateStatus === "NEEDED"}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon updateStatus={service.updateStatus} />
          </span>
          <div>
            <div class="text-f18">
              <RelativeDateLabel
                date={service.modificationDate}
                prefix="Actualisé"
                bold
              />
            </div>
            <div class="text-f14">
              Ce service n’a pas été actualisé récemment, certaines informations
              peuvent ne pas être à jour.
            </div>
          </div>
        </div>
      {:else}
        <div class="flex items-center">
          <span class="mr-s16">
            <UpdateStatusIcon updateStatus="REQUIRED" />
          </span>
          <div>
            <div class="text-f18">
              <strong>Service en attente d’actualisation</strong>
            </div>
            <div class="text-f14">
              <strong class="hidden print:inline">
                Mis à jour le
                <DateLabel date={service.modificationDate} />
              </strong>
              <span class="print:hidden">
                Les informations sur ce service n’ont plus été mises à jour
                depuis {monthDiff}
                mois.
              </span>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </div>
</div>
