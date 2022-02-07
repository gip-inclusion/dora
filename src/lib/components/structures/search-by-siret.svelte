<script>
  import Field from "$lib/components/forms/field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";

  import SiretSearch from "./siret-autocomplete.svelte";

  export let establishment;

  let city;
  export let onCityChange = null;
  export let onEstablishmentChange = null;

  function handleCityChange(newCity) {
    city = newCity;
    establishment = null;
    if (onCityChange) onCityChange(newCity);
  }

  async function handleEstablishmentChange(newEstablishment) {
    establishment = newEstablishment;
    if (onEstablishmentChange) onEstablishmentChange(newEstablishment);
  }
</script>

<Field type="custom" label="Commune" required vertical>
  <CitySearch
    slot="custom-input"
    name="city-select"
    placeholder="Saisissez et sélectionnez le nom de la ville"
    handleChange={handleCityChange}
  />
</Field>
<Field
  type="custom"
  label="Nom de votre structure ou son numéro SIRET"
  required
  vertical
>
  <SiretSearch
    slot="custom-input"
    name="siret-select"
    selectedCity={city}
    disabled={!city?.properties?.citycode}
    handleChange={handleEstablishmentChange}
    placeholder="Commencez à saisir et choisissez dans la liste"
  />
</Field>
