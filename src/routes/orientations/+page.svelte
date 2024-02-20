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
  import type { Orientation } from "$lib/types";
  import { formatLongDate } from "$lib/utils/date";
  import { formatFilePath } from "$lib/utils/file";

  export let data: PageData;
  let { orientation } = data;

  async function onRefresh() {
    orientation = (await getOrientation(orientation.queryId)) as Orientation;
  }

  onMount(() => {
    trackOrientation(orientation, $page.url);
  });
</script>

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
      class="mt-s40 flex flex-col-reverse justify-between gap-x-s24 md:flex-row"
    >
      <div class="flex flex-1 flex-col gap-s32">
        <div
          class="flex w-full items-center rounded-md border border-blue-information bg-blue-light p-s24"
        >
          <div
            class="mr-s16 inline-block rounded-xl bg-blue-information-dark p-s12"
          >
            <div class="h-s24 w-s24 fill-current text-white">
              {@html compass3Icon}
            </div>
          </div>

          <div>
            <p class="m-s0 text-f14 text-gray-text">
              Service concerné&nbsp;:<br />
              <span class="text-f23 font-bold text-france-blue">
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

        <div class="flex-[2] rounded-md border border-gray-02 md:relative">
          <div
            class="flex flex-wrap items-center justify-between gap-s12 border-b border-gray-02 px-s16 py-s20 md:px-s35"
          >
            <h2 class="m-s0 text-f23 text-france-blue">La demande</h2>
          </div>

          <div class="flex flex-col gap-s32 p-s35">
            <div>
              <SubTitle label="Bénéficiaire" icon={compass3Icon} />
              <div class="ml-s64">
                <ul class="flex flex-col gap-s12">
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
            <hr class="border border-gray-02" />

            {#if orientation.situation.length}
              <div>
                <SubTitle label="Situation" icon={listCheckIcon} />
                <div class="ml-s64">
                  <ul>
                    {#each orientation.situation as beneficiarySituation}
                      <li class="ml-s16 list-disc text-f16 text-gray-text">
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
              <hr class="border border-gray-02" />
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
                      <li class="ml-s16 list-disc text-f16 text-gray-text">
                        {requirement}
                      </li>
                    {/each}
                  </ul>
                </div>
              </div>
              <hr class="border border-gray-02" />
            {/if}

            {#if orientation.orientationReasons}
              <div>
                <SubTitle
                  label="Motifs de l’orientation"
                  icon={messageLineIcon}
                />
                <div class="ml-s64 text-f16 italic text-gray-text">
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
                        class="break-word ml-s16 list-disc text-f16 text-gray-text"
                      >
                        <a
                          href={attachment.url}
                          target="_blank"
                          rel="nofollow noopener ugc"
                          class="underline">{formatFilePath(attachment.name)}</a
                        >
                      </li>
                    {/each}
                  </ul>
                </div>
              </div>
            {/if}
          </div>
        </div>

        {#if orientation.prescriber?.name || orientation.prescriber?.email || orientation.prescriberStructure?.name}
          <div class="flex-[2] rounded-md border border-gray-02 md:relative">
            <div
              class="flex flex-wrap items-center justify-between gap-s12 border-b border-gray-02 px-s16 py-s20 md:px-s35"
            >
              <h2 class="m-s0 text-f23 text-france-blue">Les contacts</h2>
            </div>

            <div class="flex flex-col gap-s32 p-s35">
              <div>
                <SubTitle
                  label="Prescripteur ou prescriptrice"
                  icon={userSharedLineIcon}
                />
                <div class="ml-s64 text-f16 text-gray-text">
                  <ul class="flex flex-col gap-s12">
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
                <hr class="border border-gray-02" />
                <div>
                  <SubTitle
                    label="Conseiller ou conseillère référente"
                    icon={serviceIcon}
                  />
                  <div class="ml-s64 text-f16 text-gray-text">
                    <ul class="flex flex-col gap-s12">
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
        <HandleOrientation {orientation} {onRefresh} />
      </div>
    </div>
  </div></CenteredGrid
>
