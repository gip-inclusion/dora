<script context="module">
  import { getServiceAdmin } from "$lib/admin";

  export async function load({ params, fetch }) {
    const service = await getServiceAdmin(params.slug, { kitFetch: fetch });
    if (!service) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    return {
      props: {
        service: service,
      },
    };
  }
</script>

<script>
  import TextClamp from "$lib/components/text-clamp.svelte";
  import WebSearchLink from "../../_web-search-link.svelte";
  import { capitalize, markdownToHTML } from "$lib/utils";
  import InfoLine from "../../_info-line.svelte";
  import StructureContacts from "../../_structure-contacts.svelte";
  import UserInfo from "../../_user-info.svelte";
  import EmailLine from "../../_email-line.svelte";
  import SmallLink from "../../_small-link.svelte";

  import Date from "$lib/components/date.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import ModerationButtonMenu from "../../_moderation-button-menu.svelte";
  import History from "../../_history.svelte";

  export let service;
  const structure = service.structure;
  const description = markdownToHTML(service.fullDesc);

  async function handleRefresh() {
    service = await getServiceAdmin(service.slug);
  }
</script>

<svelte:head>
  <title>
    Admin | {capitalize(service.name)} | {capitalize(structure.name)} | DORA
  </title>
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="text-f12">
    <div class="flex flex-row items-baseline justify-between">
      <h2>
        <a href="/admin/services">Services</a>
        <span class="text-f10">
          <a href="#contacts">Contacts</a> |
          <a href="#infos">Informations</a>
        </span>
      </h2>
      <ModerationButtonMenu entity={service} onRefresh={handleRefresh} />
    </div>
    <h3>
      {service.name}
      <SmallLink link="/services/{service.slug}" label="front" />
      <SmallLink link="/admin/services/{service.slug}" label="admin" />
      <WebSearchLink searchString="{service.name} {structure.name}" />
    </h3>
    <InfoLine>
      Structure : <strong>{structure.name}</strong>
      <SmallLink link="/structures/{structure.slug}" label="front" />
      <SmallLink link="/admin/structures/{structure.slug}" label="admin" />
    </InfoLine>

    <h4>Historique</h4>
    <History notes={service.notes} />

    <h4 id="contacts">Contacts</h4>

    <h5>Contact du service</h5>
    <InfoLine>
      {#if service.contactName}<div>
          <strong>{service.contactName}</strong>
          <WebSearchLink
            searchString="{service.contactName} {structure.name}"
          />
        </div>
      {/if}
      {#if service.contactPhone}
        <div>📞 {service.contactPhone}</div>
      {/if}{#if service.contactcontactEmailName}
        <EmailLine email={service.contactEmail} />
      {/if}
      <div>
        informations publiques ? {service.isContactInfoPublic ? "✅" : "❌"}
      </div>
    </InfoLine>

    <InfoLine>
      créé par: <UserInfo user={service.creator} {structure} />
    </InfoLine>

    <InfoLine condition={service.creator.email !== service.lastEditor.email}>
      dernière modification par: <UserInfo
        user={service.lastEditor}
        {structure}
      />
    </InfoLine>

    <h5>Contacts de la structure</h5>

    <StructureContacts {structure} />

    <h4 id="infos">Informations</h4>

    <InfoLine>
      <div class="italic">
        {service.shortDesc}
      </div>
    </InfoLine>

    <InfoLine condition={service.fullDesc}>
      Description longue:
      <div class="prose-sm rounded-md border-2 border-gray-02 p-s16">
        <TextClamp text={description} />
      </div>
    </InfoLine>

    <InfoLine>
      thématiques: {service.categoriesDisplay}
    </InfoLine>
    <InfoLine>
      besoins: {service.subcategoriesDisplay}
      (#TODO hierarchie)
    </InfoLine>

    <InfoLine>
      frais à charge : {service.hasFee ? "✅ – " : "❌"}
      {#if service.hasFee}
        <span class="italic">{service.feeDetails}</span>
      {/if}
    </InfoLine>

    <InfoLine>
      Date de création: <Date date={service.creationDate} />
    </InfoLine>
    <InfoLine>
      Date de dernière modification: <Date date={service.modificationDate} />
    </InfoLine>

    <InfoLine>
      {#if service.model.slug}
        Model : name: {service.model.name}
        <SmallLink link="/models/{service.model.slug}" label="front" />
      {/if}
    </InfoLine>

    <InfoLine>
      périmètre : {service.diffusionZoneTypeDisplay}<br />
      territoire : {service.diffusionZoneDetailsDisplay}
    </InfoLine>

    <InfoLine>
      code postal: {service.postalCode}<br />
      ville: {service.city}<br />
      département: {service.department}
    </InfoLine>
  </div>
</CenteredGrid>
