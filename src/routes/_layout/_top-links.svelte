<script>
  import NavItem from "$lib/components/nav-item.svelte";
</script>

<nav
  class="flex flex-col items-stretch px-s16 lg:col-span-full lg:flex-row lg:px-s0"
>
  <NavItem href="/contribuer" label="Contribuer…" />
  <NavItem
    href="https://documentation.dora.fabrique.social.gouv.fr"
    label="Documentation"
    externalIcon
    otherTab
    nofollow
  />
  <NavItem
    label="Communauté de l’inclusion"
    href="https://communaute.inclusion.beta.gouv.fr/"
    externalIcon
    otherTab
  />
  <NavItem
    href="https://itou.typeform.com/doracontactsupp"
    label="Contacter l’équipe"
    externalIcon
    otherTab
    nofollow
  />
</nav>
