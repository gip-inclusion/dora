<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import EnsureLoggedIn from "$lib/components/hoc/ensure-logged-in.svelte";
  import StructureSearch from "$lib/components/specialized/establishment-search/search.svelte";
  import { siretWasAlreadyClaimed } from "$lib/requests/structures";
  import { getApiURL } from "$lib/utils/api";
  import * as v from "$lib/validation/schema-utils";
  import { structureSchema } from "$lib/validation/schemas/structure";
  import { formErrors } from "$lib/validation/validation";
  import { token } from "$lib/utils/auth";
  import { get } from "svelte/store";
  import type { Establishment, Structure } from "$lib/types";

  const schema = {
    email: {
      label: "Courriel",
      default: "",
      rules: [v.isEmail(), v.maxStrLength(254)],
      post: [v.lower, v.trim],
      maxLength: 254,
      required: true,
    },
  };

  const serverErrors = {
    _default: {},
    siret: { unique: "Cette structure existe déjà" },
  };

  const defaultStructure = Object.fromEntries(
    Object.entries(structureSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );

  let requesting = $state(false);
  let structure = $state(JSON.parse(JSON.stringify(defaultStructure)));
  let alreadyClaimedEstablishment: Structure | null = $state(null);
  let structureAdded = $state(false);

  function resetForm() {
    requesting = false;
    structure = JSON.parse(JSON.stringify(defaultStructure));
    alreadyClaimedEstablishment = null;
    structureAdded = false;
    $formErrors = {};
  }

  function handleChange(_validatedData) {}

  function handleSubmit(validatedData) {
    const url = `${getApiURL()}/auth/invite-first-admin/`;
    const method = "POST";

    return fetch(url, {
      method,
      headers: {
        Accept: "application/json; version=1.0",
        "Content-Type": "application/json",

        Authorization: `Token ${get(token)}`,
      },
      body: JSON.stringify({
        siret: validatedData.siret,
        inviteeEmail: validatedData.email,
      }),
    });
  }

  function handleSuccess(result) {
    structure = result;
    structureAdded = true;
  }

  function handleCityChange(_city) {
    structure = JSON.parse(JSON.stringify(defaultStructure));
  }

  async function establishmentAlreadyCreated(siret: string) {
    const result = await siretWasAlreadyClaimed(siret);
    if (result.ok) {
      return result.result as unknown as Structure;
    }
    return null;
  }

  async function handleEstablishmentChange(
    establishment: Establishment | null
  ) {
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
  <CenteredGrid extraClass="max-w-4xl m-auto">
    <h1 class="mb-s64 text-france-blue text-center">Ajouter une structure</h1>
    <div class="mt-s24"></div>
    {#if structureAdded && structure}
      <Notice
        title="La structure {structure.name} a été ajoutée"
        type="success"
      >
        <p class="mb-s0 text-f14">
          Une invitation pour rejoindre DORA et administrer la structure a été
          envoyée à l’adresse e-mail saisie.
        </p>
      </Notice>

      <div class="mt-s24 gap-s24 flex flex-row justify-center">
        <LinkButton
          to="/structures/{structure.slug}"
          label="Voir la structure"
          secondary
        />

        <Button onclick={resetForm} label="Ajouter une autre structure" />
      </div>
    {:else}
      <FormErrors />

      <StructureSearch
        title="Identifier la structure"
        onEstablishmentChange={handleEstablishmentChange}
        onCityChange={handleCityChange}
      />

      {#if alreadyClaimedEstablishment}
        <div class="mt-s24"></div>
        <Notice
          title="La structure {alreadyClaimedEstablishment.name} est déjà référencée sur
            DORA."
          type="info"
        >
          <p>
            {#if alreadyClaimedEstablishment.numAdmins === 0}
              Elle n’a pas encore d’administrateur.
            {:else if alreadyClaimedEstablishment.numAdmins === 1}
              Elle a déjà un administrateur.
            {:else}
              Elle compte déjà {alreadyClaimedEstablishment.numAdmins} administrateurs.
            {/if}
          </p>
          {#snippet button()}
            <LinkButton
              to="/structures/{alreadyClaimedEstablishment?.slug}"
              label="Consultez la structure"
              small
            />
          {/snippet}
        </Notice>
      {/if}

      <FormErrors />

      {#if structure.siret}
        <Form
          bind:data={structure}
          serverErrorsDict={serverErrors}
          {schema}
          onChange={handleChange}
          onSubmit={handleSubmit}
          onSuccess={handleSuccess}
          bind:requesting
        >
          <Fieldset
            title="Premier administrateur"
            descriptionText="Veuillez saisir le courriel de la personne que vous souhaitez inviter."
          >
            <BasicInputField
              type="email"
              id="email"
              bind:value={structure.email}
              descriptionText="Format attendu&nbsp;: mail@domaine.fr"
              vertical
            />
          </Fieldset>

          <div class="mt-s32 gap-s16 flex flex-col justify-end md:flex-row">
            <Button
              name="validate"
              type="submit"
              label="Envoyer l’invitation"
              disabled={requesting}
            />
          </div>
        </Form>
      {/if}
    {/if}
  </CenteredGrid>
</EnsureLoggedIn>
