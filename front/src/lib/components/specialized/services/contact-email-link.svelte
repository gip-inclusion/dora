<script lang="ts">
  import MailSendLineBusiness from "svelte-remix/MailSendLineBusiness.svelte";

  interface Props {
    email: string;
    mailtoHref?: string;
    preferred?: boolean;
  }

  const { email, mailtoHref, preferred = false }: Props = $props();

  const href = $derived(mailtoHref ?? `mailto:${email}`);
</script>

<div>
  <a
    class="text-f16 flex items-center break-all"
    class:font-bold={preferred}
    {href}
  >
    <span
      class="mr-s8 h-s24 w-s24 fill-current"
      role="img"
      aria-label="Courriel"
    >
      <MailSendLineBusiness />
    </span>
    {email}
  </a>
</div>
