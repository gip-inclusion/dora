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

  import illuRecenser from "$lib/assets/illu-recenser.svg";
  import illuMobiliser from "$lib/assets/illu-mobiliser.svg";
  import illuAccompagner from "$lib/assets/illu-accompagner.svg";

  export let servicesOptions;
</script>

<CenteredGrid --col-bg="var(--col-magenta-10)" topPadded roundedBottom>
  <div class="col-span-full mb-s40 flex flex-col gap-s24">
    <div class="text-center">
      <h1 class="text-france-blue">
        Donnez de la visibilité <br />à votre offre d’insertion
      </h1>
      <p class="mb-s0">
        Publiez et mettez à jour vos services en toute simplicité.
      </p>
    </div>
    <div class="flex justify-center gap-s16">
      <LinkButton label="Référencer un service" to={`/services/creer`} />
      <LinkButton
        label="Participer à un webinaire"
        secondary
        nofollow
        otherTab
        to={`https://app.livestorm.co/dora-1 `}
      />
    </div>

    <div class="mt-s16">
      <p class="text-center text-f12">
        Plus de 450 structures ont déjà référencé leurs services sur DORA.
      </p>
      <div class="flex justify-center gap-s24">
        <div class="flex gap-s24">
          <img src={logoPoleEmploi} alt="logo Pole Emploi" />

          <img src={logoMobIn} alt="logo Mob'In" />

          <img
            src={logoDepartementArdennes}
            alt="logo Conseil Départemental des Ardennes"
          />
        </div>
        <div class="flex gap-s24">
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

<CenteredGrid --col-bg="var(--col-transparent)" topPadded>
  <div class="col-span-full mb-s40">
    <h2 class="mb-s32 text-center text-france-blue">
      Tous les services d’insertion sur votre territoire
    </h2>
    <SearchForm {servicesOptions} />
  </div>
</CenteredGrid>

<CenteredGrid --col-bg="var(--col-transparent)" topPadded>
  <div class="col-span-full mb-s40">
    <h2 class="mb-s32 text-center text-france-blue">Comment ça fonctionne</h2>
    <div class="flex flex-col gap-s24 md:flex-row">
      <div class="md:flex-1">
        <img
          src={illuRecenser}
          alt="illustration d'un personnage avec une machine à écrire"
          class="mb-s16 w-full"
        />
        <h3>Recensement de l’offre d’insertion</h3>
        <p class="text-f16">
          Vous proposez des services d'insertion ? Renseignez votre offre sur
          DORA et touchez les acteurs de l'insertion de votre territoire.
        </p>
      </div>
      <div class="md:flex-1">
        <img
          src={illuMobiliser}
          alt="illustration d'un ordinateur avec le visage d'un personnage satisfait sur l'écran"
          class="mb-s16 w-full"
        />
        <h3>Mobilisation de service d’insertion</h3>
        <p class="text-f16">
          Vous accompagnez des bénéficiaire ? Retrouvez facilement et rapidement
          les services adaptés à vos bénéficiaires, les modalités, le bon
          contact et les bons documents à fournir.
        </p>
      </div>
      <div class="md:flex-1">
        <img
          src={illuAccompagner}
          alt="illustration avec deux personnages souriants, face à face, chacun dans une bulle qui communiquent avec leur ordinateur."
          class="mb-s16 w-full"
        />
        <h3>Accompagnement des bénéficiaires</h3>
        <p class="text-f16">
          Nous sommes tous acteurs de l'insertion ! Simplifions le retour vers
          un emploi durable des personnes qui en ont besoin.
        </p>
      </div>
    </div>
  </div>
</CenteredGrid>

<CenteredGrid --col-bg="var(--col-gray-00)">
  <div
    class="col-span-full mb-s40 mt-s32 flex flex-col items-center justify-between gap-s16 md:flex-row"
  >
    <div>
      <h3 class="mb-s8 text-gray-dark">Infolettre</h3>
      <p class="max-w-2xl text-f12 leading-relaxed text-gray-dark">
        Une fois par mois, recevez un courriel pour être informé des évolutions
        de DORA.
      </p>
    </div>

    <NewsletterButton />
  </div>
</CenteredGrid>
