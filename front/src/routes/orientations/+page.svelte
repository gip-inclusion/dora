<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";

  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import {
    attachmentIcon,
    calendarEventLineIcon,
    compass3Icon,
    homeSmile2Icon,
    inboxLineIcon,
    listCheckIcon,
    mailAddLineIcon,
    messageLineIcon,
    phoneLineIcon,
    serviceIcon,
    user6Icon,
    userSharedLineIcon,
  } from "$lib/icons";
  import { trackOrientation } from "$lib/utils/stats";
  import HandleOrientation from "./handle-orientation.svelte";
  import SubTitle from "./sub-title.svelte";
  import ContactListItem from "./contact-list-item.svelte";
  import { formatPhoneNumber } from "$lib/utils/misc";
  import { getOrientation } from "$lib/utils/orientation";
  import type { PageData } from "./$types";
  import { formatLongDate } from "$lib/utils/date";
  import { formatFilePath } from "$lib/utils/file";
  import LinkExpired from "./link-expired.svelte";

  export let data: PageData;
  const { askForNewLink, queryId, queryHash } = data;
  let { orientation } = data;

  async function onRefresh() {
    const response = await getOrientation(queryId, queryHash);
    if (response.ok) {
      orientation = response.data!;
    }
  }

  onMount(() => {
    if (orientation) {
      trackOrientation(orientation, $page.url);
    }
  });
</script>

{#if askForNewLink}
  <CenteredGrid>
    <div class="mt-s24 print:mb-s0">
      <LinkExpired {queryId} />
    </div>
  </CenteredGrid>
{:else}
  <CenteredGrid noPadding>
    <div class="mt-s24 print:mb-s0">
      <Breadcrumb currentLocation="orientation" dark />
    </div>
  </CenteredGrid>

  <CenteredGrid>
    <div>
      <h1>Demande d’orientation #{orientation.id}</h1>
      <p class="text-f16">
        <span class="font-bold">Date d’envoi de la demande&nbsp;:</span>
        {formatLongDate(orientation.creationDate)}
      </p>

      <div
        class="mt-s40 gap-x-s24 flex flex-col-reverse justify-between md:flex-row"
      >
        <div class="gap-s32 flex flex-1 flex-col">
          <div
            class="border-blue-information bg-blue-light p-s24 flex w-full items-center rounded-lg border"
          >
            <div
              class="mr-s16 bg-blue-information-dark p-s12 inline-block rounded-3xl"
            >
              <div class="h-s24 w-s24 fill-current text-white">
                {@html compass3Icon}
              </div>
            </div>

            <div>
              <p class="m-s0 text-f14 text-gray-text">
                Service concerné&nbsp;:<br />
                <span class="text-f23 text-france-blue font-bold">
                  {#if orientation.service?.slug}
                    <a
                      href="/services/{orientation.service.slug}"
                      target="_blank"
                    >
                      {orientation.service?.name}
                    </a>
                  {:else}
                    {orientation.service?.name}
                  {/if}
                </span>
              </p>
            </div>
          </div>

          {#if orientation.status !== "REFUSÉE"}
            <div class="border-gray-02 flex-2 rounded-lg border md:relative">
              <div
                class="gap-s12 border-gray-02 px-s16 py-s20 md:px-s36 flex flex-wrap items-center justify-between border-b"
              >
                <h2 class="m-s0 text-f23 text-france-blue">La demande</h2>
              </div>

              <div class="gap-s32 p-s36 flex flex-col">
                <div>
                  <SubTitle label="Bénéficiaire" icon={compass3Icon} />
                  <div class="ml-s64">
                    <ul class="gap-s12 flex flex-col">
                      <ContactListItem
                        icon={user6Icon}
                        text={`${orientation.beneficiaryFirstName} ${orientation.beneficiaryLastName}`}
                      />

                      {#if orientation.beneficiaryEmail}
                        <ContactListItem
                          icon={mailAddLineIcon}
                          text={orientation.beneficiaryEmail}
                          isPreference={orientation.beneficiaryContactPreferences.includes(
                            "EMAIL"
                          )}
                        />
                      {/if}

                      {#if orientation.beneficiaryPhone}
                        <ContactListItem
                          icon={phoneLineIcon}
                          text={formatPhoneNumber(orientation.beneficiaryPhone)}
                          isPreference={orientation.beneficiaryContactPreferences.includes(
                            "TELEPHONE"
                          )}
                        />
                      {/if}

                      {#if orientation.beneficiaryOtherContactMethod}
                        <ContactListItem
                          icon={inboxLineIcon}
                          text={`Autre méthode de contact : ${orientation.beneficiaryOtherContactMethod}`}
                          isPreference={orientation.beneficiaryContactPreferences.includes(
                            "AUTRE"
                          )}
                        />
                      {/if}

                      {#if orientation.beneficiaryAvailability}
                        <ContactListItem
                          icon={calendarEventLineIcon}
                          text={`Disponible à partir de ${formatLongDate(
                            orientation.beneficiaryAvailability
                          )}`}
                        />
                      {/if}
                    </ul>
                  </div>
                </div>

                {#if orientation.situation.length}
                  <hr class="border-gray-02 border" />
                  <div>
                    <SubTitle label="Situation" icon={listCheckIcon} />
                    <div class="ml-s64">
                      <ul>
                        {#each orientation.situation as beneficiarySituation}
                          <li class="ml-s16 text-f16 text-gray-text list-disc">
                            {#if beneficiarySituation === "Autre"}
                              {beneficiarySituation}&nbsp;: {orientation.situationOther}
                            {:else}
                              {beneficiarySituation}
                            {/if}
                          </li>
                        {/each}
                      </ul>
                    </div>
                  </div>
                  <hr class="border-gray-02 border" />
                {/if}

                {#if orientation.requirements.length}
                  <div>
                    <SubTitle
                      label="Critères auxquels le ou la bénéficiaire répond"
                      icon={listCheckIcon}
                    />
                    <div class="ml-s64">
                      <ul>
                        {#each orientation.requirements as requirement}
                          <li class="ml-s16 text-f16 text-gray-text list-disc">
                            {requirement}
                          </li>
                        {/each}
                      </ul>
                    </div>
                  </div>
                  <hr class="border-gray-02 border" />
                {/if}

                {#if orientation.orientationReasons}
                  <div>
                    <SubTitle
                      label="Motifs de l’orientation"
                      icon={messageLineIcon}
                    />
                    <div class="ml-s64 text-f16 text-gray-text italic">
                      {orientation.orientationReasons}
                    </div>
                  </div>
                {/if}

                {#if orientation.beneficiaryAttachmentsDetails?.length}
                  <div>
                    <SubTitle label="Pièces jointes" icon={attachmentIcon} />
                    <div class="ml-s64 text-gray-text">
                      <ul class="mb-s24">
                        {#each orientation.beneficiaryAttachmentsDetails as attachment}
                          <li
                            class="break-word ml-s16 text-f16 text-gray-text list-disc"
                          >
                            <a
                              href={attachment.url}
                              target="_blank"
                              rel="nofollow noopener ugc"
                              class="underline"
                              >{formatFilePath(attachment.name)}</a
                            >
                          </li>
                        {/each}
                      </ul>
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          {/if}

          {#if orientation.prescriber?.name || orientation.prescriber?.email || orientation.prescriberStructure?.name}
            <div class="border-gray-02 flex-2 rounded-lg border md:relative">
              <div
                class="gap-s12 border-gray-02 px-s16 py-s20 md:px-s36 flex flex-wrap items-center justify-between border-b"
              >
                <h2 class="m-s0 text-f23 text-france-blue">Les contacts</h2>
              </div>

              <div class="gap-s32 p-s36 flex flex-col">
                <div>
                  <SubTitle
                    label="Prescripteur ou prescriptrice"
                    icon={userSharedLineIcon}
                  />
                  <div class="ml-s64 text-f16 text-gray-text">
                    <ul class="gap-s12 flex flex-col">
                      {#if orientation.prescriber?.name}
                        <ContactListItem
                          icon={user6Icon}
                          text={orientation.prescriber?.name}
                        />
                      {/if}

                      {#if orientation.prescriber?.email}
                        <ContactListItem
                          icon={mailAddLineIcon}
                          text={orientation.prescriber?.email}
                        />
                      {/if}

                      {#if orientation.prescriberStructure?.name}
                        <ContactListItem
                          icon={homeSmile2Icon}
                          text={orientation.prescriberStructure?.name}
                          link={`/structures/${orientation.prescriberStructure?.slug}`}
                        />
                      {/if}

                      {#if orientation.referentPhone && orientation.referentEmail === orientation.prescriber.email}
                        <ContactListItem
                          icon={phoneLineIcon}
                          text={formatPhoneNumber(orientation.referentPhone)}
                        />
                      {/if}
                    </ul>
                  </div>
                </div>

                {#if orientation.referentEmail !== orientation.prescriber.email}
                  <hr class="border-gray-02 border" />
                  <div>
                    <SubTitle
                      label="Conseiller ou conseillère référente"
                      icon={serviceIcon}
                    />
                    <div class="ml-s64 text-f16 text-gray-text">
                      <ul class="gap-s12 flex flex-col">
                        <ContactListItem
                          icon={user6Icon}
                          text={`${orientation.referentFirstName} ${orientation.referentLastName}`}
                        />
                        {#if orientation.referentEmail}
                          <ContactListItem
                            icon={mailAddLineIcon}
                            text={orientation.referentEmail}
                          />
                        {/if}

                        {#if orientation.referentPhone}
                          <ContactListItem
                            icon={phoneLineIcon}
                            text={formatPhoneNumber(orientation.referentPhone)}
                          />
                        {/if}
                      </ul>
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          {/if}
        </div>

        <div class="mb-s32 w-full shrink-0 md:w-[384px]">
          <HandleOrientation {orientation} {queryHash} {onRefresh} />
        </div>
      </div>
    </div>
  </CenteredGrid>
{/if}
