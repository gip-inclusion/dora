<script lang="ts">
  import illuAccompagner from "$lib/assets/illustrations/illu-accompagner.svg";
  import illuMobiliser from "$lib/assets/illustrations/illu-mobiliser.svg";
  import illuRecenser from "$lib/assets/illustrations/illu-recenser.svg";
  import logoDataInclusion from "$lib/assets/logos/logo-data-inclusion.svg";
  import Notice from "$lib/components/display/notice.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import InviteStructureLink from "$lib/components/specialized/invite-structure-link.svelte";
  import PartnerList from "$lib/components/specialized/partner-list.svelte";
  import SearchForm from "$lib/components/specialized/service-search.svelte";
  import { externalLinkIcon } from "$lib/icons";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<CenteredGrid
  bgColor="bg-magenta-10 mb-s32 rounded-bl-[64px] rounded-br-[64px]"
>
  <h1 class="mb-s16 text-center text-france-blue">
    Identifiez rapidement les services d’insertion adaptés aux besoins de vos
    bénéficiaires
  </h1>
  <div class="mb-s32">
    <p class="text-center text-f16 text-gray-text">
      DORA vous aide dans la levée des freins périphériques bloquant le retour à
      l’emploi des bénéficiaires.
    </p>
  </div>

  <SearchForm
    servicesOptions={data.servicesOptions}
    cityCode={data.cityCode}
    cityLabel={data.cityLabel}
  />

  <div class="mb-s16 mt-s32 text-center text-f16">
    <a
      target="_blank"
      class="text-magenta-cta underline"
      rel="noopener"
      href="https://app.livestorm.co/dora-1"
    >
      Découvrez DORA en participant à un de nos webinaires d’appropriation.
    </a>
  </div>
</CenteredGrid>

<CenteredGrid>
  <Notice title="L’inclusion aujourd’hui, les défis de demain" type="success">
    <p class="text-f14">
      Le jeudi 01 février 2024, les professionnels de l’inclusion ont
      rendez-vous de 09h à 17h<br />pour un événement en ligne incontournable.
    </p>
    <div slot="button">
      <LinkButton
        to="https://www.inclusion-demain.fr/"
        label="Je m’inscris"
        icon={externalLinkIcon}
        iconOnRight
        small
        otherTab
      />
    </div>
  </Notice>
  <div class="mt-s40"></div>
  <div class="flex flex-col gap-s24">
    <div class="text-center">
      <h2 class="text-france-blue">
        Donnez de la visibilité à votre offre d’insertion
      </h2>
      <p class="mb-s0">
        Publiez, mettez à jour et rendez vos services disponibles partout grâce
        à l’<span lang="en">Open Data</span>.
      </p>
    </div>
    <div class="flex flex-wrap justify-center gap-s16">
      <LinkButton label="Référencer un service" to={`/services/creer`} />
      <InviteStructureLink />
    </div>

    <div class="mt-s16">
      <p class="text-center text-f12">
        Plus de 1 000 structures ont déjà commencé à référencer leurs services
        sur DORA
      </p>
      <ul class="mt-s24 flex w-full flex-wrap justify-center grayscale">
        <PartnerList partnersToShow={data.partnersToShow} imgHeight="small" />
      </ul>
      <div class="mt-s10 text-center">
        <a
          href="/nos-partenaires"
          class="text-center text-f18 text-magenta-cta underline"
        >
          Découvrez tous nos partenaires
        </a>
      </div>
    </div>
  </div>
</CenteredGrid>

<CenteredGrid>
  <h2 class="mb-s32 text-center text-france-blue">Comment cela fonctionne</h2>
  <div class="mb-s24 flex flex-col gap-s24 md:flex-row">
    <div class="md:flex-1">
      <img src={illuRecenser} alt="" class="mb-s16 w-full" />
      <h3>Recensement de l’offre d’insertion</h3>
      <p class="text-f16">
        Vous proposez des services d’insertion ? Rendez les visibles sur votre
        territoire et sur tous les sites partenaires grâce à notre démarche
        collective d’<span lang="en">open data</span>.
      </p>
    </div>
    <div class="md:flex-1">
      <img src={illuMobiliser} alt="" class="mb-s16 w-full" />
      <h3>Identification du service adapté</h3>
      <p class="text-f16">
        Vous accompagnez des bénéficiaires ? Trouvez rapidement les services
        d’insertion adaptés, les modalités, le bon contact et les documents à
        fournir.
      </p>
    </div>
    <div class="md:flex-1">
      <img src={illuAccompagner} alt="" class="mb-s16 w-full" />
      <h3>Mobilisation du service</h3>
      <p class="text-f16">
        Vous avez identifié le bon service ? Aidez votre bénéficiaire en
        facilitant ses démarches et son retour vers un emploi durable.
      </p>
    </div>
  </div>

  <div class="flex flex-col gap-s24 rounded-md bg-magenta-10 p-s24 md:flex-row">
    <div class="w-1/3 self-center text-center">
      <a href="https://www.data.inclusion.beta.gouv.fr/">
        <img
          src={logoDataInclusion}
          alt="Data inclusion - Contributeur officiel"
          class="inline"
        />
      </a>
    </div>
    <div class="md:w-2/3">
      <h2 class="text-f17 leading-24 text-gray-dark">Dites-le-nous une fois</h2>
      <p class="text-f16">
        Nous sommes engagés dans une démarche d’<span lang="en">Open Data</span>
        et rendons disponibles nos données à travers un référentiel commun — partagé
        par toutes les plateformes et sites web partenaires. Grâce à cette dynamique
        collective, vous référencez votre offre une seule fois tout en la rendant
        disponible partout.
      </p>
    </div>
  </div>
</CenteredGrid>
