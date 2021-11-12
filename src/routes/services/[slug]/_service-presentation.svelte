<script>
  import { userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import { lightBulbIcon } from "$lib/icons";

  import Info from "../form/_info.svelte";
  import Tag from "./_tag.svelte";

  export let service;
</script>

<style>
  h2 {
    color: var(--col-france-blue) !important;
  }

  .markdown-wrapper {
    margin-top: var(--s16);
  }

  .markdown-wrapper :global(h1),
  .markdown-wrapper :global(h2),
  .markdown-wrapper :global(h3) {
    color: var(--col-france-blue);
  }

  .markdown-wrapper :global(p) {
    color: var(--col-text);
  }

  .prose {
    max-width: 100%;
  }
</style>

<div class="flex mt-6 mb-4">
  <Tag --bg-color="var(--col-gray-01)" --fg-color="var(--col-gray-dark)">
    {service.categoryDisplay}
  </Tag>
  <div class="text-gray-text-alt2 text-xs maj ml-3">
    Mise à jour le {new Date(service.modificationDate).toLocaleDateString(
      "fr-FR",
      { year: "numeric", month: "long", day: "numeric" }
    )}
  </div>
</div>
{#if !service.structureInfo.hasAdmin}
  <Info
    title="Vous êtes le gestionaire de cet établissement ?"
    icon={lightBulbIcon}
  >
    Ces données ont été saisies par l’équipe DORA lors de l’étape
    d’expérimentation. Vous pouvez revendiquer ces contenus en créant votre
    compte et ainsi avoir la possibilité de mettre à jour les fiches de votre
    établissement.
    <div class="mt-2">
      {#if $userInfo}
        <LinkButton
          label="Demander l’accès"
          to="https://itou.typeform.com/doracontactsupp"
          nofollow
          small
        />
      {:else}
        <LinkButton
          label="Demander l’accès"
          to="/auth/inscription?siret={service.structureInfo.siret}"
          nofollow
          small
        />
      {/if}
    </div>
  </Info>
{/if}
<div class="description-wrapper">
  <div>
    <h2>Description du service</h2>
    <strong>{service.shortDesc}</strong>
    <div class="markdown-wrapper prose w-full">
      {@html service.fullDesc}
    </div>
  </div>
</div>
