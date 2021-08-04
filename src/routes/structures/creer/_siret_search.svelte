<script>
  import { getApiURL } from "$lib/utils";
  import Select from "$lib/components/forms/select.svelte";

  export let handleChange;
  export let selectedEstablishment;
  export let selectedCity;
  export let disabled;

  async function searchSirene(q) {
    const sireneAPIUrl = `${getApiURL()}/search-sirene/${
      selectedCity.value.properties.citycode
    }/?q=${encodeURIComponent(q)}`;
    const response = await fetch(sireneAPIUrl, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
    const jsonResponse = await response.json();
    console.log(jsonResponse);
    function cleanSpaces(string) {
      return string.replace(/ +/gi, " ").trim();
    }
    let results = jsonResponse.map((r) => {
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
          `${r.denominationParent} ${
            r.sigleParent ? "(" + r.sigleParent + ")" : ""
          }`
        ),
        name: cleanSpaces(
          `${r.denomination} ${
            r.enseigne1 != r.denomination ? r.enseigne1 : ""
          } ${r.enseigne2} ${r.enseigne3}`
        ),
        ape: r.ape,
        latitude: r.latitude,
        longitude: r.longitude,
      };

      if (result.name.startsWith(result.parent)) {
        result.label = result.name;
      } else {
        result.label = result.parent + " " + result.name;
      }
      result.label += " (" + result.addr1 + ")";
      return result;
    });
    console.log(results);
    return results;
  }
</script>

<Select
  onChange={handleChange}
  {disabled}
  placeholder="Nom ou SIRET"
  hideArrow
  searchFunction={searchSirene}
  delay="200"
  labelFieldName="label"
  valueFieldName="siret"
  selectedItem={selectedEstablishment}
  localSearch={false}
  minCharactersToSearch="3"
  localFiltering={false} />
