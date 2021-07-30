<script>
  import { page } from "$app/stores";
  import { token } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";

  import "../app.postcss";
</script>

<header class="shadow-md">
  <div class="flex flex-row items-center px-8 py-2">
    <a class="block" href="/">
      <img
        class="inline"
        src="/logo-ministere.png"
        alt="Accueil Ministère du Travail, de l'Emploi et de l'Insertion"
        width="107"
        height="86" />
      <img
        class="inline"
        src="/logo-dora-text.png"
        alt="Dora"
        width="86"
        height="54" />
    </a>
    <div class="flex-grow" />
    {#if $page.path !== "/login"}
      {#if $token}
        <LinkButton
          label="Deconnexion"
          to={`/logout?next=${encodeURIComponent($page.path)}`}
          secondary />
      {:else}
        <LinkButton
          label="Se connecter"
          to={`/login?next=${encodeURIComponent($page.path)}`} />
      {/if}
    {/if}
  </div>
</header>

<div class="px-8 py-2">
  <slot />
</div>
