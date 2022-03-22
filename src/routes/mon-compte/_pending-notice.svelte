<script>
  import Button from "$lib/components/button.svelte";
  import waitingPic from "$lib/assets/illus_adhesion-attente-optimise.svg";
  import Info from "$lib/components/info.svelte";
  import { adminIcon } from "$lib/icons";
  export let structure;

  const requestResent = false;

  const resendRequestFlag = false;
</script>

<div
  class="my-s24 max-w-5xl rounded-xl border border-dashed border-gray-03 px-s40"
>
  <div class="flex gap-s112 p-s40">
    <div class="flex-1">
      <h3 class="mb-s16">
        Votre adhésion à « {structure.name} » est en attente de validation par les
        responsables de votre structure.
      </h3>

      <p class="mb-s16 text-gray-text-alt2">
        Si au bout de quelques jours vous n’avez pas de réponse, vous pouvez
        relancer les responsables de votre structure.
      </p>
      {#if resendRequestFlag}
        {#if requestResent}
          <Info
            label="Votre demande a été enregistrée"
            icon={adminIcon}
            info
            whiteBg
            leftBorder
          >
            Un message à été envoyé aux responsables de votre structure.
          </Info>
        {:else}
          <Button label="Relancer les administrateurs" disabled />
        {/if}
      {/if}
    </div>
    <div class="flex-1">
      <img src={waitingPic} width="347" height="281" alt="" />
    </div>
  </div>
</div>
