<script lang="ts">
  import type { DashboardService, Service } from "$lib/types";
  import ContactEmail from "./contact-email.svelte";
  import ContactPhone from "./contact-phone.svelte";

  export let service: Service | DashboardService;
  const orientationMode = service.coachOrientationModes;
  const emailPreferred =
    service.contactEmail &&
    (orientationMode.includes("envoyer-courriel") ||
      orientationMode.includes("envoyer-fiche-prescription"));
  const phonePreferred =
    service.contactPhone && orientationMode.includes("telephoner");
  const allPreferred = emailPreferred && phonePreferred;
  const nonePreferred = !emailPreferred && !phonePreferred;
</script>

<div>
  <div class="flex flex-col gap-s4 text-f14">
    {#if service.contactName}
      <p class="mb-s6 mr-s24 text-gray-dark">
        <strong>{service.contactName}</strong>
      </p>
    {/if}
    {#if emailPreferred}
      <ContactEmail {service} preferred />
      {#if !phonePreferred}
        <p class="text-f12 text-gray-text">
          Cette structure privilégie l’e-mail comme moyen pour mobiliser ce
          service.
        </p>
      {/if}
    {/if}
    {#if phonePreferred}
      <ContactPhone {service} preferred />
      {#if !emailPreferred}
        <p class="text-f12 text-gray-text">
          Cette structure privilégie le téléphone comme moyen pour mobiliser ce
          service.
        </p>
      {/if}
    {/if}
    {#if nonePreferred}
      Pensez à consulter les <a href="#orientation-modes" class="underline"
        >conditions de mobilisation</a
      >
    {/if}

    <div class="my-s8 rounded-md bg-info-light p-s16 text-f14 text-gray-text">
      Pensez à préciser que vous avez identifié le service sur DORA 😇
    </div>

    {#if !allPreferred}
      <p class="mb-s6 mr-s24 text-gray-dark">
        {#if nonePreferred}
          <strong>Coordonnées</strong>
        {:else}
          <strong>Autres coordonnées</strong>
        {/if}
      </p>
      {#if !emailPreferred && service.contactEmail}
        <ContactEmail {service} />
      {/if}
      {#if !phonePreferred && service.contactPhone}
        <ContactPhone {service} />
      {/if}
    {/if}
  </div>
</div>
