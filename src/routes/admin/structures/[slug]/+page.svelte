<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Date from "$lib/components/utilities/date.svelte";
  import TextClamp from "$lib/components/utilities/text-clamp.svelte";
  import { getStructureAdmin } from "$lib/requests/admin";
  import { markdownToHTML } from "$lib/utils/misc";
  import History from "../../history.svelte";
  import InfoLine from "../../info-line.svelte";
  import ModerationButtonMenu from "../../moderation-button-menu.svelte";
  import SmallLink from "../../small-link.svelte";
  import StructureContacts from "../../structure-contacts.svelte";
  import UserInfo from "../../user-info.svelte";
  import WebSearchLink from "../../web-search-link.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  const description = markdownToHTML(data.structure.fullDesc);

  async function handleRefresh() {
    data.structure = await getStructureAdmin(data.structure.slug);
  }
</script>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="text-f12">
    <div class="flex flex-row items-baseline justify-between">
      <h2>
        <a href="/admin/structures">Structures</a>
        <span class="text-f10">
          <a href="#contacts">Contacts</a> |
          <a href="#infos">Informations</a>
          {#if data.structure.members.length}| <a href="#collabs">
              Collaborateurs•trices
            </a>
          {/if}
          {#if data.structure.pendingMembers.length}| <a href="#pending-collabs"
              >Collaborateurs•trices en attente</a
            >{/if}
          {#if data.structure.branches.length}| <a href="#branches">Antennes</a
            >{/if}
          {#if data.structure.models.length}| <a href="#models">Modèles</a>{/if}
          {#if data.structure.services.length}| <a href="#services">Services</a
            >{/if}
        </span>
      </h2>
      <ModerationButtonMenu entity={data.structure} onRefresh={handleRefresh} />
    </div>
    <h3>
      {data.structure.name}
      <SmallLink link="/structures/{data.structure.slug}" label="front" />
      <WebSearchLink searchString={data.structure.name} />
    </h3>

    {#if data.structure.parent.slug}
      <InfoLine>
        Antenne de <strong>{data.structure.parent.name}</strong>
        <SmallLink
          link="/structures/{data.structure.parent.slug}"
          label="front"
        />
        <SmallLink
          link="/admin/structures/{data.structure.parent.slug}"
          label="admin"
        />
      </InfoLine>
    {/if}

    <h4>Historique</h4>
    <History notes={data.structure.notes} />

    <h4 id="contacts">Contacts</h4>

    <StructureContacts structure={data.structure} />

    <h4 id="infos">Informations</h4>
    <InfoLine condition={data.structure.shortDesc}>
      <div class="italic">
        {data.structure.shortDesc}
      </div>
    </InfoLine>
    <InfoLine condition={data.structure.url}>
      <a
        href={data.structure.url}
        class="underline"
        target="_blank"
        rel="noopener nofollow">{data.structure.url}</a
      >
    </InfoLine>

    <InfoLine condition={data.structure.source}>
      source: {data.structure.source}
    </InfoLine>

    <InfoLine condition={data.structure.siret}>
      siret: {data.structure.siret}
      <SmallLink
        link="https://annuaire-entreprises.data.gouv.fr/etablissement/{data
          .structure.siret}"
        label="annuaire entreprise"
      />
      <WebSearchLink searchString={data.structure.siret} />
    </InfoLine>

    <InfoLine condition={data.structure.typologyDisplay}>
      typologie: {data.structure.typologyDisplay}
    </InfoLine>

    <InfoLine condition={data.structure.fullDesc}>
      description longue:
      <div class="prose-sm rounded-md border-2 border-gray-02 p-s16">
        <TextClamp text={description} />
      </div>
    </InfoLine>

    <InfoLine condition={data.structure.department}>
      département: {data.structure.department}
    </InfoLine>

    <InfoLine>
      adresse: {#if data.structure.longitude && data.structure.latitude}
        <SmallLink
          link="https://www.google.com/maps/search/?api=1&query={data.structure
            .latitude},{data.structure.longitude}"
          label="google map"
        />
      {/if}<br />
      {#if data.structure.address1}{data.structure.address1} <br />{/if}
      {#if data.structure.address2}{data.structure.address2}<br />{/if}
      {#if data.structure.postalCode}{data.structure.postalCode}<br />{/if}
      {#if data.structure.city}{data.structure.city}<br />{/if}
    </InfoLine>

    <InfoLine condition={data.structure.ape}>
      code APE: {data.structure.ape}
      <SmallLink
        link="https://www.insee.fr/fr/metadonnees/nafr2/sousClasse/{data
          .structure.ape}"
        label="insee"
      />
    </InfoLine>

    <InfoLine>
      date de création: <Date date={data.structure.creationDate} /><br />
      date de dernière modification: <Date
        date={data.structure.modificationDate}
      />
    </InfoLine>

    {#if data.structure.members.length}
      <h4 id="collabs">Collaborateurs•trices</h4>

      {#each data.structure.members as member}
        <InfoLine>
          <UserInfo user={member.user} structure={data.structure} />
          <strong>{member.isAdmin ? "Administrateur•trice" : ""}</strong>
        </InfoLine>
      {/each}
    {/if}

    {#if data.structure.pendingMembers.length}
      <h4 id="pending-collabs">Collaborateurs•trices en attente</h4>
      {#each data.structure.pendingMembers as member}
        <InfoLine>
          <UserInfo user={member.user} structure={data.structure} />
          <strong>{member.isAdmin ? "Administrateur•trice" : ""}</strong>
          <strong>{member.invitedByAdmin ? "Invité•e" : ""}</strong>
        </InfoLine>
      {/each}
    {/if}

    {#if data.structure.branches.length}
      <h4 id="branches">Antennes</h4>
      {#each data.structure.branches as branch}
        <div class="ml-s16">
          <h5>
            {branch.name}

            <SmallLink link="/structures/{branch.slug}" label="front" />
            <SmallLink link="/admin/structures/{branch.slug}" label="admin" />
          </h5>

          <InfoLine condition={branch.shortDesc}>
            <span class="italic">{branch.shortDesc}</span>
          </InfoLine>
        </div>
      {/each}
    {/if}

    {#if data.structure.models.length}
      <h4 id="models">Modèles</h4>

      {#each data.structure.models as model}
        <div class="ml-s16">
          <h5>
            {model.name}

            <SmallLink link="/models/{model.slug}" label="front" />
          </h5>
          <InfoLine condition={model.shortDesc}>
            <span class="italic">{model.shortDesc}</span>
          </InfoLine>
        </div>
      {/each}
    {/if}

    {#if data.structure.services.length}
      <h4 id="services">Services</h4>

      {#each data.structure.services as service}
        <div class="ml-s16">
          <h5>
            {service.name}

            <SmallLink link="/services/{service.slug}" label="front" />
            <SmallLink link="/admin/services/{service.slug}" label="admin" />
          </h5>
          <InfoLine condition={service.shortDesc}>
            <span class="italic">{service.shortDesc}</span>
          </InfoLine>
        </div>
      {/each}
    {/if}
  </div>
</CenteredGrid>
