<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchForm from "./_search-form.svelte";

  import CoverPic from "$lib/assets/illu_cover-optimise.svg";
  import MissionPic from "$lib/assets/illu_mission-optimise.svg";
  import DefinePic from "$lib/assets/illu_definir.svg";
  import ReferencePic from "$lib/assets/illu_referencer.svg";
  import JoinPic from "$lib/assets/illu_rejoindre.svg";
  import ValorisePic from "$lib/assets/illu_valoriser.svg";
  import VisiblePic from "$lib/assets/illu_visibilite.svg";
  import { arrowRightIcon } from "$lib/icons";

  export let servicesOptions;
</script>

<style>
  h1,
  h2,
  h3 {
    color: var(--col-france-blue);
  }

  h1 {
    margin-bottom: var(--s24);
    line-height: var(--s56);
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
  <div class="col-start-1 col-span-full mb-5 text-center ">
    <div class="w-1/2 mx-auto mb-8">
      <h5>
        Vous travaillez pour une structure porteuse/offreuse de services
        d'insertion ?
      </h5>
      <h2>
        Référencez votre offre de services et commencez à recevoir des demandes
        d'orientation qualifiées
      </h2>
    </div>
    <div class="flex flex-row gap-8">
      <div class="flex flex-col flex-1 ">
        <div class="mx-auto">
          <img src={VisiblePic} width="140" alt="" />
        </div>
        <h4>
          Gagnez en visibilité auprès de vos partenaires locaux et nationaux
        </h4>
      </div>
      <div class="flex flex-col flex-1">
        <div class="mx-auto">
          <img src={ValorisePic} width="140" alt="" />
        </div>
        <h4>
          Valorisez, gérez et guidez la mise à jour de votre offre de services.
          Collaborativement et à tout moment
        </h4>
      </div>
      <div class="flex flex-col flex-1">
        <div class="mx-auto">
          <img src={DefinePic} width="140" alt="" />
        </div>
        <h4>
          Définissez les modalités d'orientation de vos services, suivez et
          traitez rapidement les demandes d'orientation à un seul endroit
        </h4>
      </div>
      <div class="flex flex-col flex-1">
        <div class="mx-auto">
          <img src={ReferencePic} width="140" alt="" />
        </div>
        <h4>Référencer un service</h4>
      </div>
    </div>
    <div class="mt-6 rounded-xl bg-information-light flex flex-row p-6">
      <div class="flex-1">
        <img src={JoinPic} width="380" alt="" />
      </div>
      <div class="flex-1 text-left">
        <div class="flex flex-col gap-2 px-12">
          <h5>Rejoignez l’aventure !</h5>
          <h3>Aidez-nous à construire DORA&nbsp;!</h3>
          <p class="text-xs text-gray-text">
            Nous sommes à l’écoute de vos besoins afin de construire un service
            numérique qui vous correspond et vous permettra d’orienter plus
            facilement et rapidement vos bénéficiaires.
          </p>
          <p class="text-xs text-gray-text font-bold">
            Si vous souhaitez être tenu•e au courant de l’avancement du projet,
            participer à des tests utilisateurs ou des sessions demo, n’hésitez
            pas à vous rallier à la communauté DORA !
          </p>
          <div>
            <LinkButton
              to="https://itou.typeform.com/to/wVcrnlN9"
              label="Adhérez à la communauté"
              icon={arrowRightIcon}
              iconOnRight
              noBackground
              noPadding
              small />
          </div>
        </div>
      </div>
    </div>
  </div>
</CenteredGrid>
