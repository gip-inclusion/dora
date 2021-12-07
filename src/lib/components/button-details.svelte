<script>
  import { arrowRightSIcon } from "$lib/icons.js";
  export let label = "";
  export let details = "";
  export let type = "button";
  export let name = null;

  export let disabled = false;
</script>

<button
  {type}
  {name}
  class="px-s24 py-s12 text-f14 leading-normal border text-gray-01 border-gray-01 flex flex-row items-center justify-between text-left rounded focus:shadow-focus outline-none"
  on:click
  {disabled}
>
  <div>
    <h4 class="pb-s8 text-gray-text">{label}</h4>
    <p class="flex-auto text-gray-text-alt2 text-f14">{details}</p>
  </div>
  <div class="flex-none w-s32 h-s32 ml-s8 text-gray-text-alt fill-current">
    {@html arrowRightSIcon}
  </div>
</button>
