<script context="module">
  import { getStructureAdmin } from "$lib/admin";

  export async function load({ params, fetch }) {
    const structure = await getStructureAdmin(params.slug, { kitFetch: fetch });
    if (!structure) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    return {
      props: {
        structure,
      },
    };
  }
</script>

<script>
  import TextClamp from "$lib/components/text-clamp.svelte";
  import WebSearchLink from "../../_web-search-link.svelte";
  import { capitalize, markdownToHTML } from "$lib/utils";
  import UserInfo from "../../_user-info.svelte";
  import InfoLine from "../../_info-line.svelte";
  import StructureContacts from "../../_structure-contacts.svelte";
  import Date from "$lib/components/date.svelte";
  import SmallLink from "../../_small-link.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import ModerationButtonMenu from "../../_moderation-button-menu.svelte";
  import History from "../../_history.svelte";

  export let structure;

  const description = markdownToHTML(structure.fullDesc);

  async function handleRefresh() {
    structure = await getStructureAdmin(structure.slug);
  }
</script>

<svelte:head>
  <title>Admin | {capitalize(structure.name)} | DORA</title>
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="text-f12">
    <div class="flex flex-row items-baseline justify-between">
      <h2>
        <a href="/admin/structures">Structures</a>
        <span class="text-f10">
          <a href="#contacts">Contacts</a> |
          <a href="#infos">Informations</a>
          {#if structure.members.length}| <a href="#collabs">
              Collaborateurs•trices
            </a>
          {/if}
          {#if structure.pendingMembers.length}| <a href="#pending-collabs"
              >Collaborateurs•trices en attente</a
            >{/if}
          {#if structure.branches.length}| <a href="#branches">Antennes</a>{/if}
          {#if structure.models.length}| <a href="#models">Modèles</a>{/if}
          {#if structure.services.length}| <a href="#services">Services</a>{/if}
        </span>
      </h2>
      <ModerationButtonMenu entity={structure} onRefresh={handleRefresh} />
    </div>
    <h3>
      {structure.name}
      <SmallLink link="/structures/{structure.slug}" label="front" />
      <WebSearchLink searchString={structure.name} />
    </h3>

    {#if structure.parent.slug}
      <InfoLine>
        Antenne de <strong>{structure.parent.name}</strong>
        <SmallLink link="/structures/{structure.parent.slug}" label="front" />
        <SmallLink
          link="/admin/structures/{structure.parent.slug}"
          label="admin"
        />
      </InfoLine>
    {/if}

    <h4>Historique</h4>
    <History notes={structure.notes} />

    <h4 id="contacts">Contacts</h4>

    <StructureContacts {structure} />

    <h4 id="infos">Informations</h4>
    <InfoLine condition={structure.shortDesc}>
      <div class="italic">
        {structure.shortDesc}
      </div>
    </InfoLine>
    <InfoLine condition={structure.url}>
      <a
        href={structure.url}
        class="underline"
        target="_blank"
        rel="noopener nofollow">{structure.url}</a
      >
    </InfoLine>

    <InfoLine condition={structure.source}>
      source: {structure.source}
    </InfoLine>

    <InfoLine condition={structure.siret}>
      siret: {structure.siret}
      <SmallLink
        link="https://annuaire-entreprises.data.gouv.fr/etablissement/{structure.siret}"
        label="annuaire entreprise"
      />
      <WebSearchLink searchString={structure.siret} />
    </InfoLine>

    <InfoLine condition={structure.typologyDisplay}>
      typologie: {structure.typologyDisplay}
    </InfoLine>

    <InfoLine condition={structure.fullDesc}>
      description longue:
      <div class="prose-sm rounded-md border-2 border-gray-02 p-s16">
        <TextClamp text={description} />
      </div>
    </InfoLine>

    <InfoLine condition={structure.department}>
      département: {structure.department}
    </InfoLine>

    <InfoLine>
      adresse: {#if structure.longitude && structure.latitude}
        <SmallLink
          link="https://www.google.com/maps/search/?api=1&query={structure.latitude},{structure.longitude}"
          label="google map"
        />
      {/if}<br />
      {#if structure.address1}{structure.address1} <br />{/if}
      {#if structure.address2}{structure.address2}<br />{/if}
      {#if structure.postalCode}{structure.postalCode}<br />{/if}
      {#if structure.city}{structure.city}<br />{/if}
    </InfoLine>

    <InfoLine condition={structure.ape}>
      code APE: {structure.ape}
      <SmallLink
        link="https://www.insee.fr/fr/metadonnees/nafr2/sousClasse/{structure.ape}"
        label="insee"
      />
    </InfoLine>

    <InfoLine>
      date de création: <Date date={structure.creationDate} /><br />
      date de dernière modification: <Date date={structure.modificationDate} />
    </InfoLine>

    {#if structure.members.length}
      <h4 id="collabs">Collaborateurs•trices</h4>

      {#each structure.members as member}
        <InfoLine>
          <UserInfo user={member.user} {structure} />
          <strong>{member.isAdmin ? "Administrateur•trice" : ""}</strong>
        </InfoLine>
      {/each}
    {/if}

    {#if structure.pendingMembers.length}
      <h4 id="pending-collabs">Collaborateurs•trices en attente</h4>
      {#each structure.pendingMembers as member}
        <InfoLine>
          <UserInfo user={member.user} {structure} />
          <strong>{member.isAdmin ? "Administrateur•trice" : ""}</strong>
          <strong>{member.invitedByAdmin ? "Invité•e" : ""}</strong>
        </InfoLine>
      {/each}
    {/if}

    {#if structure.branches.length}
      <h4 id="branches">Antennes</h4>
      {#each structure.branches as branch}
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

    {#if structure.models.length}
      <h4 id="models">Modèles</h4>

      {#each structure.models as model}
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

    {#if structure.services.length}
      <h4 id="services">Services</h4>

      {#each structure.services as service}
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
