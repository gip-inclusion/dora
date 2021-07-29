<script>
  import { page } from "$app/stores";
  import { token } from "$lib/auth";

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
    {#if $token}
      <a
        class="block p-2 px-4 border rounded text-cta bg-gray-01 hover:border-dora-magenta-hover"
        href={`/logout?next=${encodeURIComponent($page.path)}`}>Deconnexion</a>
    {:else}
      <a
        class="block p-2 px-4 text-white rounded bg-cta hover:bg-dora-magenta-hover"
        href={`/login?next=${encodeURIComponent($page.path)}`}>Se connecter</a>
    {/if}
  </div>
</header>

<div class="px-8 py-2">
  <slot />
</div>
