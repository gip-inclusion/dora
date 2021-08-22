<script>
  import { getApiURL } from "$lib/utils";
  import Select from "$lib/components/forms/select.svelte";

  export let handleChange;
  export let selectedCity;
  export let disabled;
  export let name;
  export let placeholder;

  async function searchSirene(q) {
    const sireneAPIUrl = `${getApiURL()}/search-sirene/${
      selectedCity.properties.citycode
    }/?q=${encodeURIComponent(q)}`;
    const response = await fetch(sireneAPIUrl, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
    const jsonResponse = await response.json();

    function cleanSpaces(string) {
      return string.replaceAll("  ", " ").trim();
    }
    const results = jsonResponse.map((r) => {
      const result = {
        siret: r.siret,
        siren: r.siren,
        nic: r.nic,
        addr1: cleanSpaces(
          `${r.numeroVoie} ${r.repetitionIndex} ${r.typeVoie} ${r.libelleVoie}`
        ),
        addr2: r.complementAdresse,
        distrib: r.distributionSpeciale,
        city: r.libelleCedex || r.libelleCommune,
        postcode: r.codeCedex || r.codePostal,
        citycode: r.codeCommune,
        parent: cleanSpaces(
          `${r.denominationParent} ${r.sigleParent ? `(${r.sigleParent})` : ""}`
        ),
        name: cleanSpaces(
          `${r.denomination} ${
            r.enseigne1 !== r.denomination ? r.enseigne1 : ""
          } ${r.enseigne2} ${r.enseigne3}`
        ),
        ape: r.ape,
        latitude: r.latitude,
        longitude: r.longitude,
      };

      if (!result.name.startsWith(result.parent)) {
        result.name = `${result.parent} ${result.name}`;
      }
      result.label = `${result.name} (${result.addr1})`;
      return {
        value: result,
        label: result.label,
      };
    });
    return results;
  }
</script>

<Select
  onChange={handleChange}
  {disabled}
  {name}
  {placeholder}
  hideArrow
  searchFunction={searchSirene}
  delay="200"
  localFiltering={false}
  minCharactersToSearch="3">
  <span slot="postfix" let:item class="ml-1 text-gray-text-alt text-xs">
    {item.siret}
  </span>
</Select>
