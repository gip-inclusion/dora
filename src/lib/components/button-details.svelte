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
  class="flex flex-row items-center justify-between rounded border border-gray-01 px-s24 py-s12 text-left text-f14 leading-normal text-gray-01 outline-none focus:shadow-focus"
  on:click
  {disabled}
>
  <div>
    <h4 class="pb-s8 text-gray-text">{label}</h4>
    <p class="flex-auto text-f14 text-gray-text-alt2">{details}</p>
  </div>
  <div class="ml-s8 h-s32 w-s32 flex-none fill-current text-gray-text-alt">
    {@html arrowRightSIcon}
  </div>
</button>
