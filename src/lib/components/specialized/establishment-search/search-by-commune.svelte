<script lang="ts">
  import { externalLinkIcon } from "$lib/icons";
  import { getApiURL } from "$lib/utils/api";
  import CitySearch from "$lib/components/inputs/geo/city-search.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import type { Establishment, GeoApiValue } from "$lib/types";

  export let establishment;

  export let onCityChange: (newCity: GeoApiValue | null) => void;
  export let onEstablishmentChange: (estab: Establishment | null) => void;

  let queryText: string | undefined;

  let city: GeoApiValue | null;

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

  let annuaireEntreprisePath: string;
  $: {
    annuaireEntreprisePath = "";
    if (city?.code && queryText) {
      const code = city.code;
      const dept = code.slice(0, 2);
      if (["75", "69", "13"].includes(dept)) {
        annuaireEntreprisePath = `/rechercher?terme=${queryText}&cp_dep_type=dep&cp_dep=${dept}`;
      } else {
        annuaireEntreprisePath = `/rechercher?terme=${queryText}&cp_dep_type=insee&cp_dep=${code}`;
      }
    }
  }
</script>

<FieldWrapper
  id="city"
  label="Commune"
  required
  vertical
  description="Ville où la structure mène ses activités ou où elle est officiellement immatriculée. Veuillez commencer à saisir le nom de la ville et choisir parmi les options qui apparaissent."
>
  <CitySearch id="city" onChange={handleCityChange} />
</FieldWrapper>

<FieldWrapper
  id="siret-select"
  label="Dénomination"
  required
  vertical
  description="Veuillez commencer à saisir le nom de la structure et choisir parmi les options qui apparaissent."
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
    <div
      slot="itemContent"
      class="flex grow flex-row items-baseline justify-between gap-s4 px-s8 pt-s8"
      let:item
    >
      <div class="grow">
        {item.label}<br />
        <span class="text-f12 text-gray-text-alt">{item.value.address1}</span>
      </div>
      {#if item.value.isSiege}
        <div
          class="shrink-0 rounded bg-gray-01 px-s6 py-s4 text-f12 font-bold text-gray-text"
        >
          Siège
        </div>
      {/if}
      <div class="ml-s8 w-s88 text-f12 text-gray-text-alt">
        {item.value.siret}
      </div>
    </div>
  </Select>

  <p class="pt-s4 text-f14">
    Si vous avez du mal à la retrouver, consultez l’<a
      target="_blank"
      title="Ouverture dans une nouvelle fenêtre"
      rel="noopener"
      href={"https://annuaire-entreprises.data.gouv.fr" +
        annuaireEntreprisePath}
      class="inline-block h-full text-magenta-cta underline"
      >Annuaire des entreprises
      <span
        class="inline-block h-s20 w-s20 fill-current pl-s4 pt-s6"
        aria-hidden
      >
        {@html externalLinkIcon}
      </span>
    </a>
  </p>
</FieldWrapper>
