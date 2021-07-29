<script>
  import arrowRightIcon from "remixicon/icons/System/arrow-right-line.svg?raw";
  import arrowLeftIcon from "remixicon/icons/System/arrow-left-line.svg?raw";
  export let withBack, withForward, withValidate;
</script>

<div class="flex flex-row justify-center max-w-xl gap-6 p-8 mx-auto mt-8">
  {#if withBack}
    <button
      name="backward"
      type="submit"
      class="flex flex-row p-2 px-4 text-center bg-white border-2 rounded text-cta w-36 disabled:bg-gray-01 ">
      <div class="relative w-5 mr-3 fill-current top-1">
        {@html arrowLeftIcon}
      </div>
      <div>Précédent</div>
    </button>
  {/if}
  {#if withForward}
    <button
      name="forward"
      type="submit"
      class="flex flex-row w-32 p-2 px-4 text-center text-white border-2 rounded bg-cta disabled:bg-gray-01 ">
      <div>Suivant</div>
      <div class="relative w-5 ml-3 fill-current top-1">
        {@html arrowRightIcon}
      </div>
    </button>
  {/if}
  {#if withValidate}
    <button
      name="validate"
      type="submit"
      class="flex flex-row w-32 p-2 px-4 text-center text-white border-2 rounded bg-cta disabled:bg-gray-01 ">
      <div>Valider</div>
      <div class="relative w-5 ml-3 fill-current top-1">
        {@html arrowRightIcon}
      </div>
    </button>
  {/if}
</div>
