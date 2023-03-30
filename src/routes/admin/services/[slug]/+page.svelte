<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import DateLabel from "$lib/components/display/date-label.svelte";
  import TextClamp from "$lib/components/display/text-clamp.svelte";
  import { getServiceAdmin } from "$lib/requests/admin";
  import { markdownToHTML } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";
  import EmailLine from "../../email-line.svelte";
  import History from "../../history.svelte";
  import InfoLine from "../../info-line.svelte";
  import ModerationButtonMenu from "../../moderation-button-menu.svelte";
  import SmallLink from "../../small-link.svelte";
  import StructureContacts from "../../structure-contacts.svelte";
  import UserInfo from "../../user-info.svelte";
  import GoogleSearchLink from "../../google-search-link.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  const structure = data.service.structure;
  const description = markdownToHTML(data.service.fullDesc, 2);

  async function handleRefresh() {
    data.service = await getServiceAdmin(data.service.slug);
  }
</script>

<CenteredGrid>
  <div class="text-f12">
    <div class="flex flex-row items-baseline justify-between">
      <h2>
        <a href="/admin/services">Services</a>
        <span class="text-f10">
          <a href="#contacts">Contacts</a> |
          <a href="#infos">Informations</a>
        </span>
      </h2>
      <ModerationButtonMenu entity={data.service} onRefresh={handleRefresh} />
    </div>
    <h3>
      {data.service.name}
      <SmallLink link="/services/{data.service.slug}" label="front" />
      <SmallLink link="/admin/services/{data.service.slug}" label="admin" />
      <GoogleSearchLink searchString="{data.service.name} {structure.name}" />
    </h3>
    <InfoLine>
      Structure : <strong>{structure.name}</strong>
      <SmallLink link="/structures/{structure.slug}" label="front" />
      <SmallLink link="/admin/structures/{structure.slug}" label="admin" />
    </InfoLine>

    <h4>Historique</h4>
    <History notes={data.service.notes} />

    <h4 id="contacts">Contacts</h4>

    <h5>Contact du service</h5>
    <InfoLine>
      {#if data.service.contactName}<div>
          <strong>{data.service.contactName}</strong>
          <GoogleSearchLink
            searchString="{data.service.contactName} {structure.name}"
          />
        </div>
      {/if}
      {#if data.service.contactEmail}
        <EmailLine email={data.service.contactEmail} />
      {/if}
      {#if data.service.contactPhone}
        <div>📞 {data.service.contactPhone}</div>
      {/if}
      <div>
        informations publiques ? {data.service.isContactInfoPublic
          ? "✅"
          : "❌"}
      </div>
    </InfoLine>

    <InfoLine>
      créé par: <UserInfo user={data.service.creator} {structure} />
    </InfoLine>

    <InfoLine
      condition={data.service.creator.email !== data.service.lastEditor.email}
    >
      dernière modification par: <UserInfo
        user={data.service.lastEditor}
        {structure}
      />
    </InfoLine>

    <h5>Contacts de la structure</h5>

    <StructureContacts {structure} />

    <h4 id="infos">Informations</h4>

    <InfoLine>
      <div class="italic">
        {data.service.shortDesc}
      </div>
    </InfoLine>

    <InfoLine condition={data.service.fullDesc}>
      Description longue:
      <div class="prose-sm rounded-md border-2 border-gray-02 p-s16">
        <TextClamp text={description} />
      </div>
    </InfoLine>

    <InfoLine>
      thématiques: {data.service.categoriesDisplay}
    </InfoLine>
    <InfoLine>
      besoins: {data.service.subcategoriesDisplay}
      (#TODO hierarchie)
    </InfoLine>

    <InfoLine>
      frais à charge : {data.service.feeCondition}
      {#if isNotFreeService(data.service.feeCondition)}
        <span class="italic">{data.service.feeDetails}</span>
      {/if}
    </InfoLine>

    <InfoLine>
      Date de création: <DateLabel date={data.service.creationDate} />
    </InfoLine>
    <InfoLine>
      Date de dernière modification: <DateLabel
        date={data.service.modificationDate}
      />
    </InfoLine>

    <InfoLine>
      {#if data.service.model.slug}
        Model : name: {data.service.model.name}
        <SmallLink link="/models/{data.service.model.slug}" label="front" />
      {/if}
    </InfoLine>

    <InfoLine>
      périmètre : {data.service.diffusionZoneTypeDisplay}<br />
      territoire : {data.service.diffusionZoneDetailsDisplay}
    </InfoLine>

    <InfoLine>
      code postal: {data.service.postalCode}<br />
      ville: {data.service.city}<br />
      département: {data.service.department}
    </InfoLine>
  </div>
</CenteredGrid>
