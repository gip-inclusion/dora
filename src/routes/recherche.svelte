<script context="module">
  import { getServicesOptions } from "$lib/services";
  import { getApiURL } from "$lib/utils/api.js";
  import { getQuery } from "./_homepage/_search";

  async function getResults({
    categoryId,
    subCategoryId,
    cityCode,
    kindId,
    hasNoFees,
  }) {
    const query = getQuery({
      categoryId,
      subCategoryId,
      cityCode,
      kindId,
      hasNoFees,
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
    const hasNoFees = query.get("has_fee") === "0";

    return {
      props: {
        categoryId,
        subCategoryId,
        cityCode,
        cityLabel,
        kindId,
        hasNoFees,
        results: await getResults({
          categoryId,
          subCategoryId,
          cityCode,
          kindId,
          hasNoFees,
        }),
        servicesOptions: await getServicesOptions(),
      },
    };
  }
</script>

<script>
  import { onMount } from "svelte";
  import { browser } from "$app/env";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import LinkButton from "$lib/components/link-button.svelte";

  import SearchResult from "./_homepage/_search-result.svelte";
  import SearchTweakForm from "./_homepage/_search_tweak_form.svelte";
  import SearchPromo from "./_homepage/_search-promo.svelte";

  import ShareButton from "$lib/components/share-button.svelte";
  import NewsletterButton from "$lib/components/newsletter-button.svelte";
  import Tag from "$lib/components/tag.svelte";

  export let servicesOptions;
  export let categoryId, subCategoryId, cityCode, cityLabel, kindId, hasNoFees;
  export let results;

  onMount(() => {
    if (browser) {
      plausible("recherche", {
        props: {
          categoryId,
          subCategoryId,
          cityCode,
          cityLabel,
          kindId,
          hasNoFees,
        },
      });
    }
  });

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

    if (hasNoFees) {
      tags = [...tags, { label: "Sans frais à charge" }];
    }
  }
</script>

<svelte:head>
  <title
    >Services d'insertion : {tags.map((t) => t.label).join(", ")} | Recherche | DORA</title
  >
</svelte:head>

<CenteredGrid topPadded>
  <div class="col-span-full mb-s48 text-center">
    <p class="text-f16">Recherche</p>
    <h1 class="text-france-blue">Services d'insertion</h1>
    <div class="mt-s8 flex flex-row justify-center gap-s16">
      {#each tags as tag}
        <Tag>{tag.label}</Tag>
      {/each}
    </div>
  </div>
</CenteredGrid>

<CenteredGrid roundedbg>
  <div class="col-span-12 lg:col-span-4 lg:mt-s56 lg:mb-s48">
    <SearchTweakForm
      {categoryId}
      {subCategoryId}
      {cityCode}
      {cityLabel}
      {hasNoFees}
      {kindId}
      {servicesOptions}
      {radiusChoices}
    />
  </div>
  <div class="col-span-12 lg:col-span-8 lg:mt-s56">
    <div class="mt-s16 text-f14 text-gray-text-alt2">
      {results.length} résultat{#if results.length > 1}s{/if}
    </div>

    {#if results.length}
      <div class="mt-s32 flex flex-col gap-s16">
        {#each results as result}
          <SearchResult {result} />
        {/each}
      </div>
    {:else}
      <p class="text-f16 mt-s32">
        Aucun résultat ne correspond à votre recherche.<br />
        Essayez d’autres filtres.
      </p>
      <div class="lg:flex lg:gap-s24 mt-s48">
        <div
          class="p-s24 bg-white rounded-md border-gray-01 border lg:flex-1 mb-s24"
        >
          <h4>
            Vous connaissez un service d'insertion qui n'est pas référencé ?
          </h4>
          <div class="flex flex-col gap-s16">
            <LinkButton
              label="Proposer un service"
              wFull
              to="/contribuer"
              secondary
            />
            <ShareButton wFull />
          </div>
        </div>
        <div
          class="p-s24 bg-white rounded-md border-gray-01 border lg:flex-1 mb-s24"
        >
          <h4>Dora évolue rapidement. Vous souhaitez rester informé ?</h4>
          <div>
            <NewsletterButton wFull />
          </div>
        </div>
      </div>
    {/if}
    {#if categoryId === "CC"}
      <SearchPromo />
    {/if}
  </div>
</CenteredGrid>
