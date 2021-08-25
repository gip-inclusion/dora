<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchForm from "./_search-form.svelte";

  import CoverPic from "$lib/assets/illu_cover-optimise.svg";
  import MissionPic from "$lib/assets/illu_mission-optimise.svg";
  export let servicesOptions;
</script>

<style>
  h1,
  h2 {
    color: var(--col-france-blue);
  }

  h2 {
    margin-top: var(--s24);
    margin-bottom: var(--s24);
    line-height: var(--s40);
  }

  p {
    color: var(--col-text);
    font-size: var(--f16);
  }

  :global(.homepage-second-row) {
    position: relative;
    z-index: -10;
    top: -75px;
    padding-top: 80px;
  }

  .content-mission {
    margin-top: var(--s32);
  }

  .content-mission h2,
  .content-mission h5 {
    color: var(--col-white);
  }

  .content-mission p,
  .content-mission li {
    color: var(--col-gray-02);
  }

  .content-mission ul {
    margin-top: var(--s16);
    margin-bottom: var(--s16);
  }

  .content-mission li {
    margin-bottom: var(--s8);

    /* base64 encoded from remixicon/icons/System/check-line.svg,
       adding stroke="white" on the 2nd path */
    list-style-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgICA8Zz4KICAgICAgICA8cGF0aCBmaWxsPSJub25lIiBkPSJNMCAwaDI0djI0SDB6Ii8+CiAgICAgICAgPHBhdGggc3Ryb2tlPSJ3aGl0ZSIgZD0iTTEwIDE1LjE3Mmw5LjE5Mi05LjE5MyAxLjQxNSAxLjQxNEwxMCAxOGwtNi4zNjQtNi4zNjQgMS40MTQtMS40MTR6Ii8+CiAgICA8L2c+Cjwvc3ZnPgo=");
    list-style-position: inside;
  }
</style>

<CenteredGrid --col-bg="var(--col-transparent)">
  <div class="col-start-1 col-span-full mb-5">
    <div class="flex flex-row">
      <div class="flex-1">
        <h1>
          Tous les services d’insertion de votre territoire à un seul endroit.
          Mobilisables en 1 clic.
        </h1>
        <p>
          Trouvez et mobilisez rapidement le service adapté au besoin de votre
          bénéficiaire
        </p>
      </div>
      <div class="flex-1"><img src={CoverPic} alt="" /></div>
    </div>
    <SearchForm {servicesOptions} />
  </div>
</CenteredGrid>

<CenteredGrid
  gridRow="2"
  extraClass="homepage-second-row"
  --col-bg="var(--col-magenta-dark)">
  <div class="col-start-1 col-span-full mb-5">
    <div class="flex flex-row gap-8">
      <div class="flex-1">
        <img src={MissionPic} width="440" alt="" />
      </div>
      <div class="content-mission flex-1">
        <h5>La mission DORA</h5>
        <h2>Découvrir, orienter, renseigner, accompagner</h2>
        <p>
          La solution DORA est un service public numérique alimenté par les
          offreurs de services d’insertion — locaux, nationaux et numériques.
          Cette base de données centralisée permet aux accompagnateurs de
          mobiliser rapidement l’offre adaptée aux besoins de leurs
          bénéficiaires.
        </p>
        <ul>
          <li>Une recherche simple et personnalisée</li>
          <li>Des résultats qualifiés, adaptés aux besoins</li>
          <li>Des fiches solutions claires et actionnables</li>
        </ul>
      </div>
    </div>
  </div>
</CenteredGrid>

<CenteredGrid gridRow="3">
  <div class="col-start-1 col-span-full mb-5 text-center w-1/2 mx-auto">
    Vous travaillez pour une structure porteuse/offreuse de services d'insertion
    ?
    <h2>
      Référencez votre offre de services et commencez à recevoir des demandes
      d'orientation qualifiées
    </h2>
  </div>
</CenteredGrid>
<CenteredGrid gridRow="4">
  <div class="col-start-1 col-span-full mb-5">
    <LinkButton label="Voir les structures" to="/structures" noBackground />
    <LinkButton
      label="Créer une structure"
      to="/structures/creer"
      noBackground />
    <LinkButton label="Voir les services" to="/services" noBackground />
    <LinkButton label="Créer un service" to="/services/creer" noBackground />
  </div>
</CenteredGrid>
