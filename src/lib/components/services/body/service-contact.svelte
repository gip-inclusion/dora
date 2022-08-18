<script lang="ts">
  import { phoneLineIcon, mailLineIcon } from "$lib/icons";

  import type { Service } from "$lib/types";
  import { formatPhoneNumber } from "$lib/utils/phone";

  export let service: Service;
</script>

<div>
  <h2 class="mb-s24">Contact</h2>

  <div class="flex  flex-col gap-s4 text-f14 md:flex-row md:gap-s32">
    {#if service.contactName || service.contactPhone || service.contactEmail}
      {#if service.contactName}
        <p class="mb-s6 mr-s24 text-gray-dark">
          <strong>{service.contactName}</strong>
        </p>
      {/if}
      {#if service.contactPhone}
        <p class="mb-s6 mr-s24">
          <a
            class="flex items-center text-f16"
            href="tel:{service.contactPhone}"
          >
            <span
              class="mr-s8 h-s24 w-s24 text-gray-text"
              aria-label="Numéro de téléphone"
            >
              {@html phoneLineIcon}
            </span>
            {formatPhoneNumber(service.contactPhone)}
          </a>
        </p>
      {/if}
      {#if service.contactEmail}
        <p>
          <a
            class="flex items-center text-f16 underline"
            href="mailto:{service.contactEmail}"
          >
            <span class="mr-s8 h-s24 w-s24 text-gray-text" aria-label="E-mail">
              {@html mailLineIcon}
            </span>
            {service.contactEmail}
          </a>
        </p>
      {/if}
    {:else}
      <p>Aucune information de contact</p>
    {/if}
  </div>
</div>
