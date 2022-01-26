<script>
  import { browser } from "$app/env";
  import { userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import { lightBulbIcon, messageIcon } from "$lib/icons";

  import Info from "$lib/components/forms/form-info.svelte";

  import Tag from "$lib/components/tag.svelte";
  import Button from "$lib/components/button.svelte";
  import SuggestionModal from "./_suggestion-modal.svelte";

  export let service;

  let suggestionModalIsOpen = false;

  function handleSuggestion() {
    suggestionModalIsOpen = true;
    if (browser) {
      plausible("suggestion", {
        props: {
          service: service.name,
          slug: service.slug,
          structure: service.structureInfo.name,
          departement: service.department,
        },
      });
    }
  }
</script>

<SuggestionModal {service} bind:isOpen={suggestionModalIsOpen} />

<div class="flex mt-s48 mb-s32 items-baseline">
  <Tag bgColorClass="bg-gray-01" fgColorClass="text-gray-dark">
    {service.categoryDisplay}
  </Tag>
  <div class="text-gray-text-alt2 text-f12 maj ml-s24">
    Mise à jour le {new Date(service.modificationDate).toLocaleDateString(
      "fr-FR",
      { year: "numeric", month: "long", day: "numeric" }
    )}
  </div>
  <div class="flex-auto" />

  <Button
    label="Suggérer une modification"
    noBackground
    icon={messageIcon}
    iconOnRight
    small
    on:click={handleSuggestion}
  />
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
    <div class="mt-s16">
      {#if $userInfo}
        <LinkButton
          label="Demander l’accès"
          to="https://itou.typeform.com/doracontactsupp"
          otherTab
          nofollow
          small
        />
      {:else}
        <LinkButton
          label="Demander l’accès"
          to="/auth/inscription?siret={service.structureInfo.siret}"
          otherTab
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

<style lang="postcss">
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
