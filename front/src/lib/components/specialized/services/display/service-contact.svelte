<script lang="ts">
  import { userInfo } from "$lib/utils/auth";

  import type { Service, ShortService } from "$lib/types";
  import ContactEmail from "../contact-email.svelte";
  import ContactPhone from "../contact-phone.svelte";
  import MembershipPendingWarning from "$lib/components/specialized/membership-pending-warning.svelte";

  interface Props {
    service: Service | ShortService;
    useWhiteText?: boolean;
  }

  let { service, useWhiteText = true }: Props = $props();
</script>

<div>
  <div class="gap-s4 text-f14 flex flex-col" class:text-white={useWhiteText}>
    {#if $userInfo && !$userInfo.structures.length}
      <MembershipPendingWarning />
    {:else}
      {#if service.contactName}
        <p
          class="mb-s6 mr-s24"
          class:text-gray-dark={!useWhiteText}
          class:text-white={useWhiteText}
        >
          <strong>{service.contactName}</strong>
        </p>
      {/if}
      {#if service.contactEmail}
        <ContactEmail {service} preferred />
      {/if}
      {#if service.contactPhone}
        <ContactPhone {service} preferred />
      {/if}
    {/if}
  </div>
</div>
