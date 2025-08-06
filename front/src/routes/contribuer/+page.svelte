<script lang="ts">
  import AddCircleFillSystem from "svelte-remix/AddCircleFillSystem.svelte";
  import QuillPenLineDesign from "svelte-remix/QuillPenLineDesign.svelte";
  import TimerFlashLineSystem from "svelte-remix/TimerFlashLineSystem.svelte";
  import UploadCloud2LineSystem from "svelte-remix/UploadCloud2LineSystem.svelte";

  import ContributionPic from "$lib/assets/illustrations/illu-contribution.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
</script>

<CenteredGrid extraClass="bg-linear-to-b from-magenta-10 to-magenta-10/0">
  <div class="gap-s40 flex flex-wrap">
    <img
      class="flex-none"
      src={ContributionPic}
      width="587"
      height="532"
      alt=""
    />
    <div class="flex-1">
      <h1 class="text-france-blue">
        Participez à notre démarche collective en identifiant vos partenaires
      </h1>

      <p class="mb-s24 mt-s24">
        Vous pouvez des à présent contribuer à la construction de la première
        base de données publique de l’offre d’insertion nationale.
      </p>

      <LinkButton
        label="Proposer un service"
        to={"/contribuer/saisie"}
        icon={AddCircleFillSystem}
        iconOnRight
      />

      <div class="mb-s48 mt-s48 gap-s20 flex flex-col">
        <div class="flex">
          <div class="icon">
            <TimerFlashLineSystem />
          </div>
          <div class="paragraph-small">
            <strong
              >Deux minutes suffisent pour partager votre expertise&nbsp;!</strong
            >
          </div>
        </div>
        <div class="flex">
          <div class="icon">
            <QuillPenLineDesign />
          </div>
          <div class="paragraph-small">
            Complétez uniquement les informations que vous possédez sur le
            service proposé. Seuls les champs marqués d’un astérisque<span
              style="color: var(--col-error);">*</span
            > sont obligatoires.
          </div>
        </div>

        <div class="flex">
          <div class="icon">
            <UploadCloud2LineSystem />
          </div>
          <div class="paragraph-small">
            Les services renseignés sont enregistrés dans la base de données
            DORA, en attendant leur validation.
          </div>
        </div>
      </div>
    </div>
  </div>
</CenteredGrid>

<style lang="postcss">
  @reference "../../app.css";

  .icon {
    @apply mr-s12 w-s32 text-france-blue flex-none self-center fill-current;
  }
</style>
