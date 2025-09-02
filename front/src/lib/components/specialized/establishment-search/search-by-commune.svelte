<script lang="ts">
  import ExternalLinkLineSystem from "svelte-remix/ExternalLinkLineSystem.svelte";

  import CitySearch from "$lib/components/inputs/geo/city-search.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Establishment, GeoApiValue } from "$lib/types";
  import { getApiURL } from "$lib/utils/api";

  interface Props {
    establishment: Establishment | null;
    onCityChange: (newCity: GeoApiValue | null) => void;
    onEstablishmentChange: (estab: Establishment | null) => void;
  }

  let {
    establishment = $bindable(),
    onCityChange,
    onEstablishmentChange,
  }: Props = $props();

  let queryText: string = $state("");

  let city: GeoApiValue | null = $state();

  function handleCityChange(newCity: GeoApiValue | null) {
    city = newCity;
    establishment = null;
    if (onCityChange) {
      onCityChange(newCity);
    }
  }

  function handleEstablishmentChange(newEstablishment: Establishment) {
    establishment = newEstablishment;
    if (onEstablishmentChange) {
      onEstablishmentChange(newEstablishment);
    }
  }

  async function searchSirene(query) {
    if (city) {
      const url = `${getApiURL()}/search-sirene/${
        city.code
      }/?q=${encodeURIComponent(query)}`;

      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json; version=1.0",
        },
      });

      const jsonResponse = await response.json();

      const results = jsonResponse.map((result) => {
        result.label = `${result.name}`;
        return {
          value: result,
          label: result.label,
        };
      });
      return results;
    }
    return [];
  }

  let annuaireEntreprisePath: string = $derived.by(() => {
    if (city?.code && queryText) {
      const code = city.code;
      const dept = code.slice(0, 2);
      if (["75", "69", "13"].includes(dept)) {
        return `/rechercher?terme=${queryText}&cp_dep_type=dep&cp_dep=${dept}`;
      } else {
        return `/rechercher?terme=${queryText}&cp_dep_type=insee&cp_dep=${code}`;
      }
    }
    return "";
  });
</script>

<FieldWrapper
  id="city"
  label="Commune"
  required
  vertical
  descriptionText="Ville où la structure mène ses activités ou où elle est officiellement immatriculée. Veuillez commencer à saisir le nom de la ville et choisir parmi les options qui apparaissent."
>
  <CitySearch id="city" onChange={handleCityChange} />
</FieldWrapper>

<FieldWrapper
  id="siret-select"
  label="Dénomination"
  required
  vertical
  descriptionText="Veuillez commencer à saisir le nom de la structure et choisir parmi les options qui apparaissent."
>
  <Select
    id="siret-select"
    bind:searchText={queryText}
    onChange={handleEstablishmentChange}
    disabled={!city?.code}
    hideArrow
    searchFunction={searchSirene}
    delay="200"
    localFiltering={false}
    minCharactersToSearch="3"
  >
    {#snippet itemContent({ item })}
      <div
        class="gap-s4 px-s8 pt-s8 flex grow flex-row items-baseline justify-between"
      >
        <div class="grow">
          {item.label}<br />
          <span class="text-f12 text-gray-text-alt">{item.value.address1}</span>
        </div>
        {#if item.value.isSiege}
          <div
            class="bg-gray-01 px-s6 py-s4 text-f12 text-gray-text shrink-0 rounded-sm font-bold"
          >
            Siège
          </div>
        {/if}
        <div class="ml-s8 w-s88 text-f12 text-gray-text-alt">
          {item.value.siret}
        </div>
      </div>
    {/snippet}
  </Select>

  <p class="pt-s4 text-f14">
    Si vous avez du mal à la retrouver, consultez l’<a
      target="_blank"
      title="Ouverture dans une nouvelle fenêtre"
      rel="noopener"
      href={"https://annuaire-entreprises.data.gouv.fr" +
        annuaireEntreprisePath}
      class="text-magenta-cta inline-block h-full underline"
      >Annuaire des entreprises
      <span
        class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current"
        aria-hidden="true"
      >
        <ExternalLinkLineSystem class="w-s20 h-s20" />
      </span>
    </a>
  </p>
</FieldWrapper>
