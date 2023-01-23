<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import StructureSearch from "$lib/components/specialized/establishment-search/search.svelte";
  import { alertIcon } from "$lib/icons";
  import { siretWasAlreadyClaimed } from "$lib/requests/structures";
  import { structureSchema } from "$lib/validation/schemas/structure";
  import StructureEditionForm from "../structure-edition-form.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  const defaultStructure = Object.fromEntries(
    Object.entries(structureSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );
  let structure = JSON.parse(JSON.stringify(defaultStructure));
  let alreadyClaimedEstablishment;

  function handleCityChange(_city) {
    structure = JSON.parse(JSON.stringify(defaultStructure));
  }

  async function establishmentAlreadyCreated(siret) {
    const result = await siretWasAlreadyClaimed(siret);
    if (result.ok) {
      return result.result;
    }
    return false;
  }

  async function handleEstablishmentChange(establishment) {
    alreadyClaimedEstablishment = null;
    structure = JSON.parse(JSON.stringify(defaultStructure));
    if (establishment) {
      alreadyClaimedEstablishment = await establishmentAlreadyCreated(
        establishment.siret
      );
      if (!alreadyClaimedEstablishment) {
        structure.siret = establishment.siret;
        structure.name = establishment.name;
        structure.address1 = establishment.address1;
        structure.address2 = establishment.address2;
        structure.city = establishment.city;
        structure.cityCode = establishment.cityCode;
        structure.postalCode = establishment.postalCode;
        structure.ape = establishment.ape;
        structure.longitude = establishment.longitude;
        structure.latitude = establishment.latitude;
      }
    }
  }
</script>

<EnsureLoggedIn>
  <CenteredGrid>
    <h1 class="text-france-blue">Création d’une structure</h1>
  </CenteredGrid>

  <CenteredGrid>
    <StructureSearch
      onEstablishmentChange={handleEstablishmentChange}
      onCityChange={handleCityChange}
    />

    {#if alreadyClaimedEstablishment}
      <div
        class="mt-s16 flex flex-row items-center justify-center pt-s4 text-f18 text-error"
      >
        <div class="mr-s8 h-s24 w-s24 fill-current">
          {@html alertIcon}
        </div>
        <p>
          Cette structure a déjà été saisie dans DORA. Vous pouvez la
          <a
            class="underline"
            href="/structures/{alreadyClaimedEstablishment?.slug}"
          >
            visualiser
          </a>.
        </p>
      </div>
    {/if}

    {#if structure.siret}
      <StructureEditionForm
        {structure}
        structuresOptions={data.structuresOptions}
      />
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
