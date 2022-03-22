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
  import NewsletterButton from "$lib/components/newsletter-button.svelte";

  export let servicesOptions;
</script>

<CenteredGrid --col-bg="var(--col-transparent)" topPadded>
  <div class="col-span-full col-start-1 mb-s40">
    <div class="flex flex-col lg:flex-row-reverse">
      <div class="flex-1">
        <img src={CoverPic} width="600" height="400" alt="" />
      </div>
      <div class="flex-1 text-center lg:text-left">
        <h1>
          Tous les services d’insertion de votre territoire à un seul endroit.
          Mobilisables en 1 clic.
        </h1>
        <p class="pb-s16">
          Trouvez et mobilisez rapidement le service adapté au besoin de votre
          bénéficiaire
        </p>
      </div>
    </div>
    <SearchForm {servicesOptions} />
  </div>
</CenteredGrid>

<CenteredGrid
  extraClass="relative z-[-10] -top-s72 pt-s80"
  --col-bg="var(--col-magenta-dark)"
>
  <div class="col-span-full col-start-1 mb-s40">
    <div class="flex flex-col gap-s64 lg:flex-row">
      <div class="flex-1">
        <img src={MissionPic} width="440" height="420" alt="" />
      </div>
      <div class="content-mission flex-1">
        <h5>La mission DORA</h5>
        <h2>Découvrir, orienter, renseigner, accompagner</h2>

        <p>
          La solution DORA est un service public numérique alimenté par les
          offreurs de services d’insertion — locaux, nationaux et numériques.
          Base de données centralisée, DORA permet de gagner du temps en
          recherchant au même endroit tous les services dédiés à palier aux
          difficultés freinant l’insertion vers un emploi durable d’un
          bénéficiaire. Connaître la disponibilité d’un service et pouvoir le
          mobiliser en quelques clics.
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

<CenteredGrid>
  <div class="col-span-full col-start-1 mb-s40 text-center">
    <div class="mx-auto mb-s64 lg:w-1/2">
      <h5>
        Vous travaillez pour une structure porteuse/offreuse de services
        d'insertion ?
      </h5>
      <h2>
        Référencez votre offre de services et commencez à recevoir des demandes
        d'orientation qualifiées
      </h2>
    </div>
    <div class="flex flex-col gap-s64 lg:flex-row-reverse">
      <div class="flex flex-1 flex-col">
        <div class="mx-auto">
          <img src={VisiblePic} width="140" height="140" alt="" />
        </div>
        <h4>
          Gagnez en visibilité auprès de vos partenaires locaux et nationaux
        </h4>
      </div>
      <div class="flex flex-1 flex-col">
        <div class="mx-auto">
          <img src={ValorisePic} width="140" height="140" alt="" />
        </div>
        <h4>
          Valorisez, gérez et guidez la mise à jour de votre offre de services.
          Collaborativement et à tout moment
        </h4>
      </div>
      <div class="flex flex-1 flex-col">
        <div class="mx-auto">
          <img src={DefinePic} width="140" height="140" alt="" />
        </div>
        <h4>
          Définissez les modalités d'orientation de vos services, suivez et
          traitez rapidement les demandes d'orientation à un seul endroit
        </h4>
      </div>
      <div class="flex flex-1 flex-col">
        <div class="mx-auto">
          <img src={ReferencePic} width="140" height="140" alt="" />
        </div>
        <h4>Référencer un service</h4>
      </div>
    </div>
    <div
      class="mt-s48 flex flex-col rounded-xl  bg-information-light lg:flex-row lg:p-s48 "
    >
      <div class="flex-1">
        <img src={JoinPic} width="380" height="380" alt="" />
      </div>
      <div class="flex-1 text-left">
        <div class="flex flex-col gap-s16 md:px-s96">
          <h5>Rejoignez l’aventure !</h5>
          <h3 class="text-france-blue">Aidez-nous à construire DORA&nbsp;!</h3>
          <p class="text-f12 text-gray-text">
            Nous sommes à l’écoute de vos besoins afin de construire un service
            numérique qui vous correspond et vous permettra d’orienter plus
            facilement et rapidement vos bénéficiaires.
          </p>
          <p class="text-f12 font-bold text-gray-text">
            Recevez l’infolettre et suivez l’avancement du projet, participez à
            des tests utilisateurs ou des sessions de démo. N’hésitez pas à vous
            rallier à la communauté Dora&nbsp;!
          </p>
          <div>
            <LinkButton
              to="https://itou.typeform.com/doraall"
              otherTab
              nofollow
              label="Adhérer à la communauté"
              icon={arrowRightIcon}
              iconOnRight
              noBackground
              noPadding
              small
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</CenteredGrid>

<CenteredGrid --col-bg="var(--col-magenta-10)">
  <div
    class="col-span-full mb-s40 mt-s32 flex flex-col items-center justify-between gap-s16 md:flex-row"
  >
    <div>
      <h3 class="mb-s8 text-gray-dark">
        Abonnez-vous à notre lettre d’information
      </h3>
      <p class="max-w-2xl text-f12 leading-relaxed text-gray-dark">
        En renseignant votre adresse courriel, vous acceptez de recevoir nos
        actualités par courriel. Vous pouvez vous désinscrire à tout moment à
        l’aide des liens de désinscription ou en <a
          target="_blank"
          rel="noopener nofollow"
          class="underline"
          href="https://itou.typeform.com/doracontactsupp">nous contactant</a
        >.
      </p>
    </div>

    <NewsletterButton />
  </div>
</CenteredGrid>

<style lang="postcss">
  h1,
  h2 {
    color: var(--col-france-blue);
  }

  h1 {
    margin-bottom: var(--s24);
  }

  h2 {
    margin-top: var(--s24);
    margin-bottom: var(--s24);
    line-height: var(--s40);
  }

  p {
    color: var(--col-text);
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

  @screen lg {
    h1 {
      line-height: var(--s56);
    }
  }
</style>
