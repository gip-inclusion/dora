<script>
  import NavItem from "$lib/components/nav-item.svelte";
</script>

<nav class="flex flex-col col-span-full text-right md:flex-row">
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
