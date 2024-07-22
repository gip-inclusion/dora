<script lang="ts">
  import ContributionPic from "$lib/assets/illustrations/illu-contribution.svg";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import {
    addCircleIcon,
    quillPenIcon,
    timerFlashIcon,
    uploadCloudIcon,
  } from "$lib/icons";
</script>

<CenteredGrid extraClass="bg-gradient-to-b from-magenta-10 to-magenta-10/0">
  <div class="flex flex-wrap gap-s40">
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
        icon={addCircleIcon}
        iconOnRight
      />

      <div class="mb-s48 mt-s48 flex flex-col gap-s20">
        <div class="flex">
          <div class="icon">
            {@html timerFlashIcon}
          </div>
          <div class="paragraph-small">
            <strong
              >Deux minutes suffisent pour partager votre expertise&nbsp;!</strong
            >
          </div>
        </div>
        <div class="flex">
          <div class="icon">
            {@html quillPenIcon}
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
            {@html uploadCloudIcon}
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
  .icon {
    @apply mr-s12 w-s32 flex-none self-center fill-current text-france-blue;
  }
</style>
