<script lang="ts">
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";
  import { URL_HELP_SITE } from "$lib/consts";

  const aClass =
    "flex w-full lg:min-w-[200px] items-center p-s12 text-gray-text hover:text-magenta-cta hover:bg-magenta-10 rounded-sm";
</script>

<DropdownMenu>
  {#snippet label()}
    <span class="text-magenta-cta font-bold">Besoin d’aide&#8239;?</span>
  {/snippet}

  <a
    href={URL_HELP_SITE}
    target="_blank"
    rel="noopener noreferrer"
    class={aClass}
  >
    Documentation
  </a>

  <a
    href="https://www.youtube.com/@dora.inclusion/videos"
    target="_blank"
    rel="noopener noreferrer"
    class={aClass}
  >
    Tutoriels vidéos
  </a>

  <a
    href={`${URL_HELP_SITE}article/participer-a-un-webinaire-dora-h3n747/`}
    target="_blank"
    rel="noopener noreferrer"
    class={aClass}
  >
    Webinaires d’appropriation
  </a>

  <a
    href="https://docs.google.com/presentation/d/1IUAh7fqMXsrhjAE5GH7h1t7jQBSXwg6vIKO0KeRULpA/edit?slide=id.g31dc9d5c052_0_0#slide=id.g31dc9d5c052_0_0"
    target="_blank"
    rel="noopener noreferrer"
    class={aClass}
  >
    Kit de déploiement
  </a>
</DropdownMenu>
