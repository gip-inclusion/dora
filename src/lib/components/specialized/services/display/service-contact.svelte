<script lang="ts">
  import { userInfo } from "$lib/utils/auth";

  import type { Service, ShortService } from "$lib/types";
  import ContactEmail from "../contact-email.svelte";
  import ContactPhone from "../contact-phone.svelte";
  import MembershipPendingWarning from "$lib/components/specialized/membership-pending-warning.svelte";

  export let service: Service | ShortService;
  export let useWhiteText = false;
</script>

<div>
  <div class="flex flex-col gap-s4 text-f14" class:text-white={useWhiteText}>
    {#if $userInfo && !$userInfo.structures.length}
      <MembershipPendingWarning />
    {:else}
      {#if service.contactName}
        <p class="mb-s6 mr-s24 text-gray-dark" class:text-white={useWhiteText}>
          <strong>{service.contactName}</strong>
        </p>
      {/if}
      {#if service.contactEmail}
        <ContactEmail {service} preferred />
      {/if}
      {#if service.contactPhone}
        <ContactPhone {service} preferred />
      {/if}
      {#if !service.contactEmail && !service.contactPhone}
        Informations de contact non renseignées
      {/if}
    {/if}
  </div>
</div>
