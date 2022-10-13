<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  import SearchForm from "./_search-form.svelte";

  import NewsletterButton from "$lib/components/newsletter-button.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import logoPoleEmploi from "$lib/assets/logo-pole-emploi.svg";
  import logoMobIn from "$lib/assets/logo-mob-in.svg";
  import logoDepartementArdennes from "$lib/assets/logo-departement-ardennes.svg";
  import logoDepartementReunion from "$lib/assets/logo-departement-reunion.svg";
  import logoAfpa from "$lib/assets/logo-afpa.svg";
  import logoCaf from "$lib/assets/logo-caf.svg";
  import logoDataInclusion from "$lib/assets/data-inclusion-logo.svg";

  import illuRecenser from "$lib/assets/illu-recenser.svg";
  import illuMobiliser from "$lib/assets/illu-mobiliser.svg";
  import illuAccompagner from "$lib/assets/illu-accompagner.svg";

  export let servicesOptions;
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
      l'emploi des bénéficiaires.
    </p>
  </div>

  <SearchForm {servicesOptions} />

  <div class="mt-s32 mb-s16 text-center text-f16">
    <a
      target="_blank"
      class="text-magenta-cta underline"
      rel="no-follow"
      href="https://app.livestorm.co/dora-1"
    >
      Découvrez DORA en participant à un de nos webinaires d’appropriation.
    </a>
  </div>
</CenteredGrid>

<CenteredGrid>
  <div class="flex flex-col gap-s24">
    <div class="text-center">
      <h2 class="text-france-blue">
        Donnez de la visibilité à votre offre d’insertion
      </h2>
      <p class="mb-s0">
        Publiez, mettez à jour et rendez vos services disponibles partout grâce
        à l'Open Data.
      </p>
    </div>
    <div class="flex justify-center">
      <LinkButton label="Référencer un service" to={`/services/creer`} />
    </div>

    <div class="mt-s16">
      <p class="text-center text-f12">
        Plus de 1 000 structures ont déjà commencé à référencer leurs services
        sur DORA
      </p>
      <div class="flex flex-col justify-center gap-s24 md:flex-row">
        <div class="flex justify-center gap-s24">
          <img src={logoPoleEmploi} alt="logo Pole Emploi" />

          <img src={logoMobIn} alt="logo Mob'In" />

          <img
            src={logoDepartementArdennes}
            alt="logo Conseil Départemental des Ardennes"
          />
        </div>
        <div class="flex justify-center gap-s24">
          <img
            src={logoDepartementReunion}
            alt="logo Conseil départemental de la Réunion"
          />

          <img src={logoAfpa} alt="logo Afpa" />

          <img src={logoCaf} alt="logo Allocations Familiales" />
        </div>
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
        Vous proposez des services d'insertion ? Rendez les visibles sur votre
        territoire et sur tous les sites partenaires grâce à notre démarche
        collective d'open data.
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
        <img src={logoDataInclusion} alt="logo data inclusion" class="inline" />
      </a>
    </div>
    <div class="md:w-2/3">
      <h4>Dites-le-nous une fois</h4>
      <p class="text-f16">
        Nous sommes engagés dans une démarche d’Open Data et rendons disponibles
        nos données à travers un référentiel commun — partagé par toutes les
        plateformes et sites web partenaires. Grâce à cette dynamique
        collective, vous référencez votre offre une seule fois tout en la
        rendant disponible partout.
      </p>
    </div>
  </div>
</CenteredGrid>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="flex flex-col items-center justify-between gap-s16 md:flex-row">
    <div>
      <h3 class="mb-s8">Infolettre</h3>
      <p class="text-f16">
        Une fois par mois, recevez un courriel pour être informé des évolutions
        de DORA.
      </p>
    </div>

    <NewsletterButton />
  </div>
</CenteredGrid>
