<script context="module">
  import { getServicesOptions } from "$lib/services";
  import { getApiURL } from "$lib/utils/api.js";
  import { getQuery } from "./_homepage/_search";
  import { trackSearch } from "$lib/utils/plausible.js";

  async function getResults({
    categoryId,
    subCategoryId,
    cityCode,
    kindId,
    fee,
  }) {
    const query = getQuery({
      categoryId,
      subCategoryId,
      cityCode,
      kindId,
      fee,
    });
    const url = `${getApiURL()}/search/?${query}`;

    const res = await fetch(url, {
      headers: { Accept: "application/json; version=1.0" },
    });

    if (res.ok) {
      return await res.json();
    }

    // TODO: log errors
    try {
      console.error(await res.json());
    } catch (err) {
      console.error(err);
    }
    return [];
  }

  const radiusChoices = [
    { value: "10", label: "10 km" },
    { value: "20", label: "20 km" },
    { value: "50", label: "50 km" },
    { value: "100", label: "100 km" },
  ];

  export async function load({ url }) {
    const query = url.searchParams;
    const categoryId = query.get("cat");
    const subCategoryId = query.get("sub");
    const cityCode = query.get("city");
    const cityLabel = query.get("cl");
    const kindId = query.get("kinds");
    const fee = query.get("fee");

    const services = await getResults({
      categoryId,
      subCategoryId,
      cityCode,
      kindId,
      fee,
    });
    trackSearch(
      categoryId,
      subCategoryId,
      cityCode,
      cityLabel,
      kindId,
      fee,
      services.length
    );
    return {
      props: {
        categoryId,
        subCategoryId,
        cityCode,
        cityLabel,
        kindId,
        fee,
        services,
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchResult from "./_homepage/_search-result.svelte";
  import SearchTweakForm from "./_homepage/_search_tweak_form.svelte";
  import SearchPromo from "./_homepage/_search-promo.svelte";

  import EmailButton from "$lib/components/email-button.svelte";
  import NewsletterButton from "$lib/components/newsletter-button.svelte";
  import Tag from "$lib/components/tag.svelte";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { NPS_FORM_ID } from "$lib/const";

  export let servicesOptions;
  export let categoryId, subCategoryId, cityCode, cityLabel, kindId, fee;
  export let services;

  let tags = [];

  $: {
    tags = [];

    if (categoryId) {
      const categoryTag = servicesOptions.categories.find(
        (c) => c.value === categoryId
      );

      if (categoryTag) {
        tags = [categoryTag];
      }

      if (categoryTag && subCategoryId) {
        const subCategoryTag = servicesOptions.subcategories.find(
          (c) => c.value === subCategoryId
        );

        if (subCategoryTag) {
          tags = [...tags, subCategoryTag];
        }
      }
    }

    if (cityLabel) {
      tags = [...tags, { label: cityLabel }];
    }

    if (kindId) {
      const kindTag = servicesOptions.kinds.find((c) => c.value === kindId);

      if (kindTag) {
        tags = [...tags, kindTag];
      }
    }

    if (fee) {
      tags = [...tags, { label: "Frais à charge" }];
    }
  }
</script>

<svelte:head>
  <title>
    Services d’insertion : {tags.map((t) => t.label).join(", ")} | Recherche | DORA
  </title>
  <meta name="robots" content="noindex" />
</svelte:head>

<CenteredGrid>
  <div class="text-center">
    <p class="text-f16">Recherche</p>
    <h1 class="text-france-blue">Services d’insertion</h1>
    <div class="mt-s8 flex flex-row justify-center gap-s16">
      {#each tags as tag}
        <Tag>{tag.label}</Tag>
      {/each}
    </div>
  </div>
</CenteredGrid>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="flex flex-col gap-s24 lg:flex-row">
    <div class="lg:mb-s48 lg:w-1/3">
      <SearchTweakForm
        {categoryId}
        {subCategoryId}
        {cityCode}
        {cityLabel}
        {fee}
        {kindId}
        {servicesOptions}
        {radiusChoices}
      />
    </div>
    <div class="lg:w-2/3">
      <div class="mt-s16 text-f14 text-gray-text-alt2">
        {services.length}
        {services.length > 1 ? "résultats" : "résultat"}
      </div>

      {#if services.length}
        <div class="mt-s32 flex flex-col gap-s16">
          {#each services as service}
            <SearchResult result={service} />
          {/each}
        </div>
      {:else}
        <p class="mt-s32 text-f16">
          Aucun résultat ne correspond à votre recherche.<br />
          Essayez d’autres filtres.
        </p>
        <div class="mt-s48 lg:flex lg:gap-s24">
          <div
            class="mb-s24 rounded-md border border-gray-01 bg-white p-s24 lg:flex-1"
          >
            <h4>
              Vous connaissez un service d’insertion qui n'est pas référencé ?
            </h4>
            <div class="flex flex-col gap-s16">
              <LinkButton
                label="Proposer un service"
                wFull
                to="/contribuer"
                secondary
              />
              <EmailButton wFull />
            </div>
          </div>
          <div
            class="mb-s24 rounded-md border border-gray-01 bg-white p-s24 lg:flex-1"
          >
            <h4>Dora évolue rapidement. Vous souhaitez rester informé ?</h4>
            <div>
              <NewsletterButton wFull />
            </div>
          </div>
        </div>
      {/if}
      {#if ["famille--garde-enfants", "famille--accompagnement-parents"].includes(subCategoryId)}
        <SearchPromo />
      {/if}
    </div>
  </div>
</CenteredGrid>

<TallyNpsPopup formId={NPS_FORM_ID} />
