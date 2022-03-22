<script>
  import { loginIcon, userFillIcon } from "$lib/icons.js";

  import LinkButton from "$lib/components/link-button.svelte";
  import TopLinks from "./_top-links.svelte";
  import { shortenString } from "$lib/utils";

  export let structures;
</script>

<LinkButton
  label="Mon compte"
  to={`/mon-compte`}
  icon={userFillIcon}
  iconOnRight
  noBackground
/>

<LinkButton
  label="Déconnexion"
  to={`/auth/deconnexion`}
  icon={loginIcon}
  iconOnRight
  noBackground
/>

<div class="block lg:hidden">
  {#if !!structures?.length}
    <hr class="my-s16 border-t border-gray-01" />
    <div class="flex flex-col items-start">
      {#each structures as structure}
        <LinkButton
          label={shortenString(structure.name, 24)}
          to={`/structures/${structure.slug}`}
          noBackground
          small
        />
      {/each}
    </div>
  {/if}
  <hr class="my-s16 border-t border-gray-01" />
  <TopLinks />
</div>
