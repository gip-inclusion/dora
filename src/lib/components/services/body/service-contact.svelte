<script lang="ts">
  import { phoneLineIcon, mailLineIcon } from "$lib/icons";

  import type { DashboardService, Service } from "$lib/types";
  import { formatPhoneNumber } from "$lib/utils/phone";

  export let service: Service | DashboardService;
  export let presentation: "inline" | "block" = "block";

  const isInline = presentation === "inline";
</script>

<div>
  <h2 class="mb-s24" class:inline-title={isInline}>Contact</h2>

  <div
    class="flex flex-col gap-s4 text-f14 md:flex-row md:gap-s32"
    class:inline-container={isInline}
  >
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

<style lang="postcss">
  .inline-title {
    @apply mr-s48 mb-s0 inline-flex text-f23;
  }
  .inline-container {
    @apply inline-flex items-center md:gap-s24 lg:gap-s32;
  }
  .inline-container p {
    @apply m-s0 mr-s10;
  }
</style>
