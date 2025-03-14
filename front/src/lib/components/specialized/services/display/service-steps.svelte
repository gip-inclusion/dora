<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import Button from "$lib/components/display/button.svelte";
  import Linkify from "$lib/components/display/linkify.svelte";
  import {
    copyIcon,
    externalLinkIcon,
    mailLineIcon,
    mapPinFillIcon,
    phoneFillIcon,
  } from "$lib/icons";
  import type {
    BeneficiaryAccessModes,
    CoachOrientationModes,
    Model,
    Service,
  } from "$lib/types";
  import { token } from "$lib/utils/auth";

  export let service: Service | Model;

  const orderedCoachOrientationModeValues: Record<
    CoachOrientationModes,
    number
  > = {
    "formulaire-dora": 0,
    "envoyer-un-mail-avec-une-fiche-de-prescription": 1,
    "completer-le-formulaire-dadhesion": 2,
    "envoyer-un-mail": 3,
    telephoner: 4,
    autre: 5,
  };

  const orderedBeneficiariesAccessModeValues: Record<
    BeneficiaryAccessModes,
    number
  > = {
    "se-presenter": 0,
    "completer-le-formulaire-dadhesion": 1,
    "envoyer-un-mail": 2,
    telephoner: 3,
    professionnel: 4,
    autre: 5,
  };

  const dispatch = createEventDispatcher<{
    trackMobilisation: { externalUrl?: string };
    showPreventFakeOrientationModal: object;
  }>();

  let isContactInfoForProfessionalShown = false;
  let isContactInfoForIndividualShown = false;

  function trackMobilisationUnconditionally(externalUrl: string) {
    dispatch("trackMobilisation", { externalUrl });
  }

  function showContactInfoForProfessional() {
    if (!$token && !service.isContactInfoPublic) {
      goto(
        `/auth/connexion?next=${encodeURIComponent(
          $page.url.pathname + $page.url.search
        )}`
      );
      return;
    }
    dispatch("trackMobilisation", {});
    isContactInfoForProfessionalShown = true;
  }

  function showContactInfoForIndividual() {
    dispatch("trackMobilisation", {});
    isContactInfoForIndividualShown = true;
  }

  $: contactInfoForIndividual =
    service.isContactInfoPublic ||
    (service.beneficiariesAccessModes ?? []).some((mode) =>
      ["envoyer-un-mail", "telephoner"].includes(mode)
    );
  $: contactInfoForIndividualAddress = [
    service.structureInfo.address1,
    service.structureInfo.address2,
    service.structureInfo.postalCode,
    service.structureInfo.city,
  ]
    .filter(Boolean)
    .join(", ");
  $: contactInfoForIndividualPhone =
    service.contactPhone || service.structureInfo.phone;
  $: contactInfoForIndividualEmail =
    service.contactEmail || service.structureInfo.email;

  $: coachOrientationModesValueAndDisplay = (
    service.coachOrientationModes ?? []
  )
    .map((val, index) => [val, service.coachOrientationModesDisplay[index]])
    .sort(
      (a, b) =>
        orderedCoachOrientationModeValues[a[0]] -
        orderedCoachOrientationModeValues[b[0]]
    );

  $: beneficiariesAccessModesValueAndDisplay = (
    service.beneficiariesAccessModes ?? []
  )
    .map((val, index) => [val, service.beneficiariesAccessModesDisplay[index]])
    .sort(
      (a, b) =>
        orderedBeneficiariesAccessModeValues[a[0]] -
        orderedBeneficiariesAccessModeValues[b[0]]
    );
</script>

<section class="gap-s24 flex flex-col">
  <h2 class="text-f23 text-france-blue mb-s0 leading-32 font-bold">
    Les démarches à réaliser
  </h2>
  <section>
    <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
      Pour les professionnels de l’accompagnement
    </h3>
    <ul class="text-gray-text space-y-s2 list-inside list-disc">
      {#each coachOrientationModesValueAndDisplay as [modeValue, modeDisplay] (modeValue)}
        <li>
          {#if modeValue === "formulaire-dora"}
            Orienter votre bénéficiaire via le formulaire DORA
          {:else if modeValue === "envoyer-un-mail-avec-une-fiche-de-prescription" && "contactEmail" in service}
            Envoyer un email avec une fiche de prescription
            {#if isContactInfoForProfessionalShown}
              <a
                href={`mailto:${service.contactEmail}`}
                class="text-magenta-cta underline">{service.contactEmail}</a
              >
            {:else}
              <button
                on:click={showContactInfoForProfessional}
                class="text-magenta-cta underline">Voir l’adresse email</button
              >
            {/if}
          {:else if modeValue === "completer-le-formulaire-dadhesion"}
            <a
              href={service.coachOrientationModesExternalFormLink}
              target="_blank"
              on:click={() =>
                trackMobilisationUnconditionally(
                  service.coachOrientationModesExternalFormLink
                )}
              class="text-magenta-cta underline"
              >{service.coachOrientationModesExternalFormLinkText ||
                "Orienter votre bénéficiaire"}
              <span class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current"
                >{@html externalLinkIcon}</span
              ></a
            >
          {:else if modeValue === "autre"}
            <Linkify
              text={service.coachOrientationModesOther}
              on:linkClick={(event) =>
                trackMobilisationUnconditionally(event.detail.url)}
            />
          {:else}
            {modeDisplay}
          {/if}
          {#if modeValue === "envoyer-un-mail" && "contactEmail" in service}
            {#if isContactInfoForProfessionalShown}
              <a
                href={`mailto:${service.contactEmail}`}
                class="text-magenta-cta underline">{service.contactEmail}</a
              >
            {:else}
              <button
                on:click={showContactInfoForProfessional}
                class="text-magenta-cta underline">Voir l’adresse email</button
              >
            {/if}
          {:else if modeValue === "telephoner" && "contactPhone" in service}
            {#if isContactInfoForProfessionalShown}
              <a
                href={`tel:${service.contactPhone}`}
                class="text-magenta-cta underline">{service.contactPhone}</a
              >
            {:else}
              <button
                on:click={showContactInfoForProfessional}
                class="text-magenta-cta underline"
                >Voir le numéro de téléphone</button
              >
            {/if}
          {/if}
        </li>
      {:else}
        <li>Non renseigné</li>
      {/each}
    </ul>
  </section>
  <section>
    <h3 class="text-f17 leading-s24 text-gray-dark mb-s8 font-bold">
      Pour les particuliers
    </h3>
    <ul class="text-gray-text space-y-s2 list-inside list-disc">
      {#each beneficiariesAccessModesValueAndDisplay as [modeValue, modeDisplay] (modeValue)}
        <li>
          {#if modeValue === "completer-le-formulaire-dadhesion"}
            <a
              href={service.beneficiariesAccessModesExternalFormLink}
              target="_blank"
              on:click={() =>
                trackMobilisationUnconditionally(
                  service.beneficiariesAccessModesExternalFormLink
                )}
              class="text-magenta-cta underline"
              >{service.beneficiariesAccessModesExternalFormLinkText ||
                "Faire une demande"}
              <span class="h-s20 w-s20 pl-s4 pt-s6 inline-block fill-current"
                >{@html externalLinkIcon}</span
              ></a
            >
          {:else if modeValue === "professionnel"}
            Orientation par un professionnel
          {:else if modeValue === "autre"}
            <Linkify
              text={service.beneficiariesAccessModesOther}
              on:linkClick={(event) =>
                trackMobilisationUnconditionally(event.detail.url)}
            />
          {:else}
            {modeDisplay}
          {/if}
        </li>
      {:else}
        <li>Non renseigné</li>
      {/each}
    </ul>
    {#if contactInfoForIndividual}
      <div class="border-gray-02 p-s24 mt-s24 rounded-2xl border shadow-sm">
        {#if isContactInfoForIndividualShown}
          <h5>{service.structureInfo.name}</h5>
          <ul class="space-y-s8 text-gray-text">
            {#if contactInfoForIndividualAddress}
              <li class="gap-s16 flex items-center">
                <span
                  class="h-s28 w-s28 bg-service-blue p-s6 text-france-blue inline-block rounded-full"
                  role="img"
                  aria-label="Adresse">{@html mapPinFillIcon}</span
                >
                {contactInfoForIndividualAddress}
              </li>
            {/if}
            {#if contactInfoForIndividualPhone}
              <li class="gap-s16 flex items-center">
                <span
                  class="h-s28 w-s28 bg-service-blue p-s6 text-france-blue inline-block rounded-full"
                  role="img"
                  aria-label="Téléphone">{@html phoneFillIcon}</span
                >
                <span class="gap-s6 flex items-center"
                  >{contactInfoForIndividualPhone}<Button
                    on:click={() =>
                      navigator.clipboard.writeText(
                        contactInfoForIndividualPhone
                      )}
                    icon={copyIcon}
                    label="Copier le numéro de téléphone"
                    hideLabel
                    small
                    noBackground
                    noPadding
                  /></span
                >
              </li>
            {/if}
            {#if contactInfoForIndividualEmail}
              <li class="gap-s16 flex items-center">
                <span
                  class="h-s28 w-s28 bg-service-blue p-s6 text-france-blue inline-block rounded-full"
                  role="img"
                  aria-label="Email">{@html mailLineIcon}</span
                >
                <span class="gap-s6 flex items-center"
                  >{contactInfoForIndividualEmail}<Button
                    on:click={() =>
                      navigator.clipboard.writeText(
                        contactInfoForIndividualEmail
                      )}
                    icon={copyIcon}
                    label="Copier l’adresse email'"
                    hideLabel
                    small
                    noBackground
                    noPadding
                  /></span
                >
              </li>
            {/if}
          </ul>
        {:else}
          <Button
            on:click={showContactInfoForIndividual}
            label="Afficher les coordonnées"
          />
        {/if}
      </div>
    {/if}
  </section>
</section>
